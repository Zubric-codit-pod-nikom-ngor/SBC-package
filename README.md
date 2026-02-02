# SBC-package
This is the module for working with blockchain. It has some problems like circular topology or the fact that it has a temporary server (not really a problem but it bothers me) but i think it will be patched later. 

basic setup to create your own blockchain:
```python
import sbc_package as sbc
from threading import Thread

blockchain = sbc.BlockChain()
thrd = Thread(target=blockchain.create,daemon=True)
thrd.start()

#////////////////////////////////
#here you can make your own logic
#////////////////////////////////
```

example of joining to any blockchain:
```python
import sbc_package as sbc
from threading import Thread

#ip of temporary server of blockchain you desire
ip: str = "127.0.0.1"

blockchain = sbc.BlockChain()
thrd = Thread(target=blockchain.join,
              daemon=True,args=(ip,))
thrd.start()

#////////////////////////////////
#your own logic here
#////////////////////////////////
```

getting the data from blockchain is done by using ```sbc_package.BlockChain().chain.fetch_current()```, ```.fetch_version()``` or ```.fetch_period()```. Also you can add blocks by using ```sbc_package.BlockChain().chain.add_block()```

Warning! Do NOT try to interfere with module files or your blockchain data will probably never work because of encryption of core file, i repeat DO NOT change core files
