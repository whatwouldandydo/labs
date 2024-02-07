# Summary

SSH key authentication allows to access the remote devices without entering a password by using RSA public and private keys as authencation.

Example: Device A gives B its RSA public key. Device A accesses B via SSH and authenticate B with its private key.

</br>

## Remote SSH and Visual Code Tool

1. On local machine, generate a RSA key. Use naming convention when dealing with multiple remote devices and RSAs.

        ssh-keygen -t rsa -b 4096 -f Users/<Name>/.ssh/<rsa_key_name>

2. On the local machine, copy the Public key `<rsa_key_name>.pub` to the remote device.

        scp Users/<Name>/.ssh/<rsa_key_name>.pub username@remote.dns:~/.ssh/

3. On the remote device, change the public key to `authorized_keys` and change file permission.

        cat ~/.ssh/<rsa_key_name>.pub >> authorized_keys

        chmod 600 ~/.ssh/authorized_keys

4. In VSCode, install `Remote - SSH` extension and add remote host information to `Users/<Name>/.ssh/config`. Private key file is the one without the .pub `~/.ssh/<rsa_key_name>`


        Host name.dns
        HostName 1.1.1.1
        User teddy
        IdentityFile Users\<Name>\.ssh\config\<rsa_key_name>

</br>

#

## Visual Code and GitHub SSH Key Authencation

1. Install git tool. For Windows, install `Git Bash`. For Linux, `apt-get git`.

2. On local machine, generate a RSA key. Use email and naming convention when dealing with multiple remote devices and RSAs.

        ssh-keygen -t rsa -b 4096 -C "user@email.com" -f Users/<Name>/.ssh/<rsa_key_name>

3. On local machine, start the SSH Agent.

        eval $(ssh-agent -s)

4. On local machine, add the SSH private key.

        ssh-add ~/.ssh/<rsa_key_name>

5. Copy the local machine public key and add it to GitHub > Settings > SSH and GPG keys

        clip < ~/.ssh/<rsa_key_name>.pub

6. If there's GitHub permission error *permission denied (publickey)*, add these commands to `.bashrc` or `.bash_profile`.

        eval $(ssh-agent -s)
        ssh-add ~/.ssh/<rsa_key_name>


#
