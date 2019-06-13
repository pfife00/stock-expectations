
<h3>Setting up Passwordless SSH</h3>

<h4>kafka-master</h4>

<code>sudo apt install openssh-server openssh-client</code>

<code>cd ./.ssh/</code>

<code>ssh-keygen -t rsa-P “” </code>

<code>id_rsa</code>

<code>cat id_rsa.pub</code>
cat id_rsa.pub

Copy text

Test out connection
<code>ssh -i ~/.ssh/id_rsa ubuntu@slave ip address</code>

<code>ssh ubuntu@slave ip address</code>


<h4>kafka-1</h4>
<code>nano ./.ssh/authorized_keys</code>

paste copied text after existing key and save

<h4>kafka-2</h4>
<code>nano ./.ssh/authorized_keys</code>

paste copied text after existing key and save

<h4>kafka-3</h4>
<code>nano ./.ssh/authorized_keys</code>

paste copied text after existing key and save



```python

```
