import subprocess
import os
import re

class GitRep:
    def __init__(self, local=False, clone=False):
        work_path = os.getcwd()
        if clone:
            self._initRemote(clone)
        elif local:
            self._initLocal(local)
        os.chdir(work_path)
        self._parse_status()

    def _initLocal(self, localrep_name): 
        if not os.path.exists(localrep_name):
            os.mkdir(localrep_name)
            os.chdir(localrep_name)
            result = subprocess.run(['git', 'init'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                print(result.stdout.decode('utf-8'))
            else:
                print(result.stderr.decode('utf-8'))
        elif not os.path.exists(localrep_name + '/.git'):
            raise ValueError('Ooops.' + localrep_name + ' already exists and it is not repo')
        else:
            os.chdir(localrep_name)
        self.rep_path = os.getcwd()

    def _initRemote(self, remrep_link):
        result = subprocess.run(['git', 'clone', remrep_link], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            rep_init_out = result.stderr.decode('utf-8')
            print(rep_init_out)
            rel_rep_path = rep_init_out.split("'")[1]
            os.chdir(rel_rep_path)
            self.rep_path = os.getcwd()
        else:
            raise ValueError(remrep_link + 'looks wrong, try to fix link or install ssh key. \n The error is: \n' + result.stderr.decode('utf-8'))


    def _parse_status(self):
        self.new_files = []
        self.mod_files = []
        self.del_files = []
        self.untracked_files = []
        status = self.git_status()
        self.cur_branch = re.findall('On branch (\S+)', status)
        self.new_files = re.findall('new files:\s+(\S+)', status)
        self.mod_files = re.findall('modified:\s+(\S+)', status)
        self.del_files = re.findall('deleted:\s+(\S+)', status)
        untrack_files = re.search('Untracked files:\s+.+(?:\s+(\S+))*', status)
        if untrack_files:
            self.untracked_files = re.findall(r'\t(\S+)', untrack_files.group())


    def git_status(self):
        if os.getcwd() != self.rep_path:
            work_path = os.getcwd()
        else:
            work_path = self.rep_path
        os.chdir(self.rep_path)
        result = subprocess.run(['git', 'status'], stdout=subprocess.PIPE)
        if result.returncode == 0:
            os.chdir(work_path)
            return result.stdout.decode('utf-8')
        else:
            os.chdir(work_path)
            raise ValueError('Something is wrong. Reinit class')

    def git_checkout(self, branch_name):
        if os.getcwd() != self.rep_path:
            work_path = os.getcwd()
        else:
            work_path = self.rep_path
        os.chdir(self.rep_path)
        result = subprocess.run(['git', 'checkout', branch_name], stdout=subprocess.PIPE)
        print(result.stdout.decode('utf-8'))
        if result.returncode == 0:
            os.chdir(work_path)
            self._parse_status()
            return result.stdout.decode('utf-8')
        else:
            os.chdir(work_path)
            raise ValueError('Something is wrong. Reinit class')
       

    def git_branch(self, branch_name):
        if os.getcwd() != self.rep_path:
            work_path = os.getcwd()
        else:
            work_path = self.rep_path
        os.chdir(self.rep_path)
        result = subprocess.run(['git', 'branch', branch_name], stdout=subprocess.PIPE)
        print(result.stdout.decode('utf-8'))
        if result.returncode == 0:
            self._parse_status()
            os.chdir(work_path)
            return result.stdout
        else:
            os.chdir(work_path)
            raise ValueError('Something is wrong. Reinit class')

    def git_commit(self, commit_message):
        if os.getcwd() != self.rep_path:
            work_path = os.getcwd()
        else:
            work_path = self.rep_path
        os.chdir(self.rep_path)
        subprocess.run(['git', 'add', '.'])
        result = subprocess.run(['git', 'commit', '-m', commit_message], stdout=subprocess.PIPE)
        print(result.stdout.decode('utf-8'))
        if result.returncode == 0:
            self._parse_status()
            os.chdir(work_path)
            return result.stdout.decode('utf-8')
        else:
            os.chdir(work_path)
            raise ValueError('Something is wrong. Resolve the issues')

    def git_push(self):
        if os.getcwd() != self.rep_path:
            work_path = os.getcwd()
        else:
            work_path = self.rep_path
        os.chdir(self.rep_path)
        result = subprocess.run(['git', 'push'], stdout=subprocess.PIPE)
        print(result.stdout.decode('utf-8'))
        if result.returncode == 0:
            os.chdir(work_path)
            self._parse_status()
            return result.stdout
        else:
            os.chdir(work_path)
            raise ValueError('Something is wrong. Resolve the issues')
