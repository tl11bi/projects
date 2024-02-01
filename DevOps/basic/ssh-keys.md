# generate ssh keys and add to authentication

```bash
# generate ssh keys with ssh-keygen
ssh-keygen -t rsa -C connorli0@outlook.com
# add ssh keys to authentication
eval `ssh-agent -s`
# delete all ssh keys
ssh-add -D
# add ssh keys to authentication
ssh-add ~/.ssh/id_rsa
# copy ssh pub to authorized_keys
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
```

## github
    
```bash
git config --global credential.helper store
git config --global --list
git config --global --list --show-origin
```
sample ~/.gitconfig
```text
[user]
    name = connor, li
    email = connorli0@outlook.com
[credential]
    helper = store
```

add password
```bash
touch .git-credentials
cat "https://connorli0:password@github" >> ~/.git-credentials
```

# check the host name 
```bash
hostname
# ip address
hostname -I
```

```bash
# setup root password
sudo passwd root
``````