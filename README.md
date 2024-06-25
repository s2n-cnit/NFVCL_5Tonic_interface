# "NFVCL 5Tonic Interface" (NTI)
The "NFVCL 5Tonic Interface" (NAI) is the south-bound component to allow NFVCL to interact with 5Tonic 5G core subsystem (named "spanish exFa" in the "5G-Induce" project, [5G-Induce project](https://www.5g-induce.eu/)) .

## NFVCL
The NFVCL is a network-oriented meta-orchestrator, specifically designed for zeroOps and continuous automation. 
It can create, deploy and manage the lifecycle of different network ecosystems by consistently coordinating multiple 
artefacts at any programmability levels (from physical devices to cloud-native microservices).
A more detailed description of the NFVCL will be added to the [Wiki](https://nfvcl-ng.readthedocs.io/en/latest/index.html).

## How does it work
--

## Getting started
After download the code, follow the steps below:
- Configure "athonethost.txt" and "imsilist.txt":
  - "fivetonichost.txt": IP address and port of the 5Tonic interface
    ``` bash
    # fivetonichost.txt
    127.0.0.1
    8500
    ```
- Execute the "setup.sh" script. It download and install all the software needed for the execution of the "NFVCL Athonet Interface".
  ``` bash
  ./setup.sh
  ```
- Lauch "run.sh". This script creates two screens where the code will be in execution.
  ``` bash
  ./run.sh
  ```



## Authors
**Guerino Lamanna**

- GitHub: [@guerol](https://github.com/guerol)

## Mantenairs
**Guerino Lamanna**

- GitHub: [@guerol](https://github.com/guerol)

## Contributing

Contributions, issues, and feature requests are welcome!

## 📝 License

This project is [GPL3](./LICENSE) licensed.
