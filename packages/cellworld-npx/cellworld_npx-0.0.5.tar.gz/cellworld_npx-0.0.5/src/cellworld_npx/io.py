import numpy as np
from kilosort import run_kilosort
from time import sleep
from .probe import create_kilosort_probe
from datetime import datetime
from glob import glob
import os
import subprocess
import getpass


def find_file(folder, fstr, joined=False):
    for root,dirs,files in os.walk(folder):
        files = [f for f in files if fstr in f]
        if len(files) > 0:
            if joined:
                return [os.sep.join([root, f]) for f in files]
            else:
                return root, files
        
def find_files(folder, filestr, foldstr=''):
    """
    Lists files containing "fstr" in directory "folder". Optionally filter folders containing "foldstr".
    """
    d = []
    for root,dirs,files in os.walk(folder):
        file = [f for f in files if filestr in f]
        if (len(file) > 0) & (foldstr in root):
            d.append({'root': root, 'files': file})
    return d

def split_path(path):
    path = os.path.normpath(path)
    parts = path.split(os.sep)
    return parts

def walk_back(path, x:str):
    parts = split_path(path)
    i = [i for i in range(len(parts)) if x in parts[i]]
    assert len(i) == 1, f'multiple parent directories containing {x} found'
    return os.sep.join(parts[0:i[0]+1])

def match_date(dates, date, threshold=5*60):
    dt = np.abs(np.array([(date - t).total_seconds() for t in dates]))
    if any(dt < threshold):
        return np.argmin(dt)

def get_session_folders(sess_path=str):
    spk_path,_ = find_file(sess_path, 'cluster_group')
    beh_path,_ = find_file(sess_path, 'experiment.json')

    assert len(beh_path) > 0, f'No behavioral data found in {sess_path}'
    assert len(spk_path) > 0, f'No curated spike data found in {sess_path}'

    return spk_path, beh_path

def get_session_paths(sess_path=str):
    spk_path = find_files(sess_path, 'cluster_group')
    beh_path = find_files(sess_path, 'experiment.json')

    assert len(beh_path) > 0, f'No behavioral data found in {sess_path}'
    assert len(spk_path) > 0, f'No curated spike data found in {sess_path}'

    spk_paths = [f['root'] for f in spk_path]
    beh_paths = [f['root'] for f in beh_path]

    return spk_paths, beh_paths

def match_experiment_date(target_experiment, path_list=list, delta_t=3600):
    if type(target_experiment) != datetime:
        target_date = get_experiment_datetime(target_experiment)
    else:
        target_date = target_experiment
    dates = [get_experiment_datetime(p) for p in path_list]
    time_delta = [(d - target_date).total_seconds() for d in dates]
    candidate_experiments = [p for i,p in enumerate(path_list) if (np.abs(time_delta[i]) < delta_t)]
    return candidate_experiments

def get_experiment_datetime(experiment=str):
    if '\\\\' in experiment:
        experiment = experiment.split('\\\\')[-1]
    if '\\' in experiment:
        experiment = experiment.split('\\')[-1]
    return datetime.strptime('_'.join(experiment.split('_')[1:3]), '%Y%m%d_%H%M')

def match_session_paths(spike_folder=str, behavior_database='D:\\behavior', sort=False, pre=-5, post=60):
    spk_path = find_files(spike_folder, 'cluster_group')
    if (len(spk_path) == 0) & sort:
        binary_files = find_files(spike_folder, 'continuous.dat', 'Neuropix-PXI')
        print(f"{len(binary_files)} binary files found in {spike_folder}")
        for file in binary_files:
            print(f"\nRUNNING KILOSORT FOR {os.path.split(file['root'])[-1]}... this may take some time!")
            sleep(1)
            run_ks(file['root'], file['root'])
        spk_path = find_files(spike_folder, 'cluster_group')
    if len(spk_path) == 0:
        print(f'Warning: No curated spike data found in {spike_folder}, run kilosort.')
        spk_path = find_files(spike_folder, 'structure')

    # get behavioral sessions close to current spike session
    mouse = spike_folder.split(os.sep)[-2]
    spike_date = datetime.strptime(spike_folder.split(os.sep)[-1], '%Y-%m-%d_%H-%M-%S')
    path_list = os.listdir(behavior_database)
    path_list = [p for p in path_list if mouse in p and not os.path.isfile(os.path.join(behavior_database,p))]
    behavior_dates = [datetime.strptime('_'.join(p.split('_')[1:3]), '%Y%m%d_%H%M') for p in path_list]
    time_delta = [(b - spike_date).total_seconds() for b in behavior_dates]
    candidate_sessions = [p for i,p in enumerate(path_list) if (time_delta[i] > pre*60) & (time_delta[i] < post*60)]

    # check if any other spike sessions are a better match to the candidates
    spike_files = os.listdir(os.sep.join(spike_folder.split(os.sep)[:-1]))
    spike_files = [s for s in spike_files if '_BAD' not in s]
    spike_dates = [datetime.strptime(f.split(os.sep)[-1], '%Y-%m-%d_%H-%M-%S') for f in spike_files]
    candidates = [datetime.strptime('_'.join(c.split('_')[1:3]), '%Y%m%d_%H%M') for c in candidate_sessions]
    mn = []
    for c in candidates:
        mn.append(np.min(np.abs([(c - sd).total_seconds() for sd in spike_dates])))
    better_candidates = np.array(mn) < np.min(np.abs(time_delta))
    if any(better_candidates):
        candidate_sessions = [c for i,c in enumerate(candidate_sessions) if not better_candidates[i]]

    spk_paths = [f['root'] for f in spk_path]
    beh_paths = [os.path.join(behavior_database, s) for s in candidate_sessions]
    
    return spk_paths, beh_paths

def get_episode_folders(behavior_path, return_valid=True):
    p = behavior_path

    if type(p) == list:
        folders = []
        episodes = []
        counter = 0
        for path in p:
            tmp = glob(os.path.join(path, 'episode_*'))
            folders.extend(tmp)
            episodes.extend([int(f.split(os.sep)[-1].split('_')[-1]) + counter for f in tmp])
            counter = counter + len(tmp)
    else:
        folders = glob(os.path.join(p, 'episode_*'))
        episodes = [int(f.split(os.sep)[-1].split('_')[-1]) for f in folders]

    if not return_valid:
        episode_is_valid = [1] * len(folders)
        return folders, episodes, episode_is_valid
    
    return get_valid_episodes(folders, episodes)

def get_valid_episodes(folders=list(), episodes=list()):
    valid_folders = []
    valid_episodes = []
    episode_is_valid = []
    sync_data_present = []
    for i,f in enumerate(folders):
        episode_file = glob(os.path.join(f, '*episode*.json'))
        sync_file = glob(os.path.join(f, '*sync*.json'))
        if (len(episode_file) > 0) & (len(sync_file) > 0):
            valid_folders.append(f)
            valid_episodes.append(episodes[i])
            episode_is_valid.append(1)
        else:
            episode_is_valid.append(0)
        if (len(sync_file) > 0):
            sync_data_present.append(1)
    return valid_folders, valid_episodes, episode_is_valid, sync_data_present

def run_ks(data_dir, results_dir=None, probe=None):
    if results_dir is None:
        results_dir = os.path.join(data_dir, '..', '..')
    if probe is None:
        root = os.path.join(data_dir, '..', '..', '..', '..')
        xml = [os.path.join(root, f) for f in os.listdir(root) if 'settings.xml' in f]
        assert len(xml) > 0, f'No settings.xml file found in {root}, must provide probe object to use for sorting!'
        probe = create_kilosort_probe(xml[0])

    settings = {'data_dir': data_dir, 'results_dir': results_dir, 'n_chan_bin':probe['n_chan']}
    ops, st, clu, tF, Wall, similar_templates, is_ref, est_contam_rate, kept_spikes = \
        run_kilosort(settings=settings, probe=probe)

def run_powershell(command):
    process = subprocess.Popen(
        ["powershell.exe", "-Command", "-"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(command)
    
    if stderr:
      print(f"Error: {stderr}")
    return stdout

def mount_drive(drive_letter='Z:', network_path='\\\\resfiles.northwestern.edu\\DOMBECK_LAB', username='ads\\cfa3244'):
    password = getpass.getpass("Enter password: ")
    command = f'net use {drive_letter} "{network_path}" {password} /user:{username}'
    output = run_powershell(command)
    if 'success' in output:
       print(f'Drive mounted to {drive_letter}')

def backup_folder(folder, source='D:\\', remote='Z:\\Dombeck_Lab_Data_Backup\\Chris Angeloni\\spikes\\'):
   command = f'rclone copy {source}{folder}\\ "{remote}\\{folder}" -P --exclude "/System Volume Information/**"'
   print('BACKING UP DATA USING THE FOLLOWING COMMAND:')
   print(f'\t{command}')
   output = run_powershell(command)
   print(output)

def start_kilosort(mouse_name, source='D:\\'):
    binary_files = find_files(os.path.join(source, mouse_name), 'continuous.dat', 'Neuropix-PXI')
    for f in binary_files:
        spike_files = find_files(f['root'], 'cluster_group')
        if len(spike_files) == 0:
            print(f"\nRUNNING KILOSORT FOR {os.path.split(f['root'])[-1]}... this may take some time!")
            sleep(1)
            run_ks(f['root'], f['root'])
        else:
            print(f"\nKILSORT RESULTS FOUND IN {os.path.split(f['root'])[-1]}... skipping!")

def run_kilosort_and_upload(mouse_name, source='D:\\', remote='Z:\\Dombeck_Lab_Data_Backup\\Chris Angeloni\\spikes\\', username='ads\\cfa3244'):
    if type(mouse_name) is not list:
        mouse_name = [mouse_name]

    for m in mouse_name:
        start_kilosort(m, source=source)
        backup_folder(m, source=source, remote=remote)
