import git


class Repo(git.Repo):

    def get_latest_changes_on_master(self):
        self.heads.master.checkout()
        self.remote(name='origin').pull()
        self.head.reset(index=True, working_tree=True)
        self.git.clean('-f')

    def has_matching_branch(self):
        for head in self.heads:
            head.checkout()
            if not self.is_dirty():
                return True
        return False

    def commit_push_branch(self, branch_name, commit_message, author):
        self.create_head(branch_name).checkout()
        self.git.commit('-m', commit_message, author=author)
        self.git.push('--set-upstream', 'origin', branch_name)

    def stage_everything(self):
        self.git.add(all=True)
