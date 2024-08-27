# "NFVCL 5Tonic Interface" (NTI)
The "NFVCL 5Tonic Interface" (NTI) is the south-bound component to allow NFVCL to interact with 5Tonic 5G core subsystem (named "spanish exFa" in the "5G-Induce" project, [5G-Induce project](https://www.5g-induce.eu/)) .

## NFVCL
The NFVCL is a network-oriented meta-orchestrator, specifically designed for zeroOps and continuous automation. 
It can create, deploy and manage the lifecycle of different network ecosystems by consistently coordinating multiple 
artefacts at any programmability levels (from physical devices to cloud-native microservices).
A more detailed description of the NFVCL will be added to the [Wiki](https://nfvcl-ng.readthedocs.io/en/latest/index.html).


## Workflow
It is possible to execute three operations using the NTI: "check slice", "add slice" and "del slice".
The first operation is just to check if a specific slice (using a name as search key) yet exist in the system.
Then using the "add slice" request, a slice can be instantiated. 
The 5 Tonic 5G core accepts the following parameters for every slice:
- coverage area (indoor or outdoor)
- latency in ms 
- uplink throughput in bps
- downlink throughput in bps
  
The slice creation is executed in two steps: "onboarding" (a group of preliminary operations) and the definitive "instantiation".
```
Slice Onboarding -> Slice Instantiation
```

Similarly the "del slice" operation is also composed by two subsequent functions: "terminate" and "delete".
```
Slice Termintate -> Slice Delete
```


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
