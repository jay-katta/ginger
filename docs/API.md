## Project Ginger REST API Specification

The Ginger API provides all functionalities of the plugin that may be used
directly by external tools. In the following sections you will find the
specification of all Collections and Resource types that are supported and
URIs where they can be accessed. As Ginger API uses Wok (Webserver Originated
from Kimchi) framework, it uses the same general conventions of Kimchi. In order
to use the API effectively, please consider the following general conventions
(from Kimchi documentation):

* The **Content Type** of the API is JSON.  When making HTTP requests to this
  API you should specify the following headers:
    * Accept: application/json
    * Content-type: application/json
* A **Collection** is a group of Resources of a given type.
    * A **GET** request retrieves a list of summarized Resource representations
      This summary *may* include all or some of the Resource properties but
      *must* include a link to the full Resource representation.
    * A **POST** request will create a new Resource in the Collection. The set
      of Resource properties *must* be specified as a JSON object in the request
      body.
    * No other HTTP methods are supported for Collections
* A **Resource** is a representation of a singular object in the API
    * A **GET** request retrieves the full Resource representation.
    * A **DELETE** request will delete the Resource. This request *may* contain
      a JSON object which specifies optional parameters.
    * A **PUT** request is used to modify the properties of a Resource
    * A **POST** request commits an *action* upon a Resource. The request body
      *must* contain a JSON object which specifies parameters.
* URIs begin with a '/plugins/ginger' to indicate the root of the Ginger API.
    * Variable segments in the URI begin with a ':' and should replaced with the
      appropriate resource identifier.

### Collection: Tasks

**URI:** /plugins/ginger/tasks

**Methods:**

* **GET**: Retrieve a summarized list of current Ginger specific tasks (stored
in Ginger's object store)

### Resource: Task

**URI:** /plugins/ginger/tasks/*:id*

A task represents an asynchronous operation that is being performed by the
server.

**Methods:**

* **GET**: Retrieve the full description of the Task
    * id: The Task ID is used to identify this Task in the API.
    * status: The current status of the Task
        * running: The task is running
        * finished: The task has finished successfully
        * failed: The task failed
    * message: Human-readable details about the Task status
    * target_uri: Resource URI related to the Task
* **POST**: *See Task Actions*

**Actions (POST):**

*No actions defined*


### Resource: Configuration

**URI:** /plugins/ginger/config

Contains information about Ginger configuration.

**Methods:**

* **GET**: Retrieve configuration information
    * version: The version of the Ginger plugin
* **POST**: *See Configuration Actions*

**Actions (POST):**

*No actions defined*


### Resource: Firmware (Power System firmware)

**URI:** /plugins/ginger/firmware

**Methods:**

* **GET**: Retrieve the current firmware levels.
    * level: The firmware levels (MI and ML, or Maint. Level)
             The final group is the currently booted firmware.
**Actions (POST):**

* commit: Commit the image running on the temp side to the perm side.
          In order to do this, the machine must be running the temp image.
* reject: Reject the image on the temp side, overwriting it with
          the image from the perm side. In order to do this, the machine must
          be running the permanent image.
* upgrade: Update the firmware level of the booted side.
    * path: The remote file path pointing to the firmware image file.
    * overwrite-perm: Indicate whether possibly overwriting the permanent boot
                      side while updating the firmware is acceptable. A value
                      of 'False' guarantees the current perm side image remains
                      untouched. Note: If running permanent image, this will
                      result in an error. It is optional.


### Resource: FirmwareProgess (Power System firmware)

**URI:** /plugins/ginger/fwprogress

**Methods:**

* **GET**: Retrieve the output of the update_flash execution.


### Collection: SAN Adapters (Fibre Channel SCSI Hosts - HBAs)

**URI:** /plugins/ginger/san_adapters

**Methods:**

* **GET**: Retrieve a summarized list with the names of all defined fibre
           channel scsi hosts found in the server system.

### Resource: SAN Adapter (Fibre Channel SCSI Host - HBA)

**URI:** /plugins/ginger/san_adapters/*:name*

**Methods:**

* **GET**: Retrieve many information from a given SAN Adapter
    * name: The name of the adapter in the system (usually "hostXX").
    * wwpn: World Wide Port Name of the adapter.
    * wwnn: World Wide Node Name of the adapter.
    * state: Indicates the current state of the adapter port (eg. Online or
             Offline).
    * max_vports: Maximum number of virtual ports supported in a NVIP (N-port
                  ID virtualization) configuration by the adapter.
    * vports_inuse: Number of virtual ports being used in a NVIP configuration.
    * speed: Transfer speed being used by the adapter (eg. 1 Gbit, 2 Gbit, 4
             Gbit, 8 Gbit, or more).
    * symbolic_name: HBA overview information.

### Resource: Sensors

**URI:** /plugins/ginger/sensors

**Methods:**

* **GET**: Get sensors data for devices on the system, including
            CPU temperatures, fan speeds, and hard disk temperatures.
            This command uses lm-sensors, so it will return all
            sensor data located in sysfs files, or in the sensors.conf
            file, if it has been created by the system admin.

            Note: The default unit for temperature is Celsius. This
            can be changed to Fahrenheit in ginger.conf.

            Due to the large number of sensors in existence, and the
            user's ability to customize sensor names, the output
            will vary greatly from system to system. The only consistency
            will be the json items named 'sensors' and 'hdds'
    * sensors: Each sensor or sensor group returned by 'sensors', depending on
            whether there are multiple sensors on a chip. For example, a CPU
            may return a package temperature reading (along with a min, max,
            critical, and alarm temps) and additional readings for each core.
            If fan speeds are reported by lm-sensors, these will be returned
            as well. The last element of each device will be its unit, instead
            of appending a unit to each value.
            Note: Power supplies may report a negative value, which is valid.
    * hdds: The temperatures for disk drives in the system, returned by hddtemp.
            These will be in the format { "/dev/sda":102.0 } for each drive.
            The last item in the list will be a the temperature unit.

### Resource: IBM Serviceable Event Provider (SEP)

**URI:** /plugins/ginger/ibm_sep

**Methods:**

* **GET**: Retrieve a dictionary with the SEP status and subscription information:
    * status: Status of the SEP agent. Can be 'running' or 'not running'.
    * subscription: Dictionaries with the SEP subscription information:
        * hostname: Hostname of the host server.
        * port: Number of the network port used by the SEP agent.
        * community: SNMP community name which host server is member.
* **PUT**: Create and/or update a subscription

*Actions (POST):**

* start: Start the SEP daemon on host server.
* stop: Stop the SEP daemon on host server.

### Resource: IBM Serviceable Event Provider (SEP)

**URI:** /plugins/ginger/ibm_sep

**Methods:**

* **GET**: Retrieve a dictionary with the SEP status and subscription information:
    * status: Status of the SEP agent. Can be 'running' or 'not running'.
    * subscription: Dictionaries with the SEP subscription information:
        * hostname: Hostname of the host server.
        * port: Number of the network port used by the SEP agent.
        * community: SNMP community name which host server is member.
* **PUT**: Create and/or update a subscription

*Actions (POST):**

* start: Start the SEP daemon on host server.
* stop: Stop the SEP daemon on host server.

### Collection: File Systems

URI: /plugins/ginger/filesystems

**Methods:**

* **GET**: Retrieve a summarized list of all mounted filesystems

* **POST**: Mount a local or NFS file system
       * type : type of filesystem. Value should be local or NFS.

    For a local file system mount:
       * blk_dev : Path of the device to be mounted.
       * mount_point : Mount point for the filesystem.

    For NFS mount:
       * server : ip address of the remote NFS server
       * share : location of the remote share
       * mount_point : Mount point for the filesystem

### Resource: File System

URI: /plugins/ginger/filesystems/*:mount_point*

*Methods:**

* **GET**: Retrieve the full description of the mounted filesystem

       * use%: Percentage of the filesystem used
       * used: Amount of space used in filesystem
       * size:  Total size of the filesystem
       * mounted_on: Mount point of the filesystem
       * avail : Total space available on the filesystem
       * filesystem : Name of the filesystem.
       * type : Filesystem type.

* **DELETE**: Unmount the Filesystem

### Resource: Network Interface Configuration

**URI:** /plugins/ginger/network/cfginterfaces/*:name*

**Methods:**

* **GET**: Retrieve the information available in network interface
           file /etc/sysconfig/network-scripts/ifcfg-<name>
    * BASIC_INFO: Basic information of network interface:
        * NAME: Name of the interface.
        * DEVICE: Device name of the interface.
        * ONBOOT: 'Yes' if interface is to be brought up during boot,
                  'No' if interface should not be brought up during boot.
        * TYPE: Interface type (Ethernet,Bond,Vlan)
        * MACADDR: Mac address of ethernet device.
        * VLAN: 'Yes' If its vlan device.
        * VLAN_ID: Vland of the vlan device.
        * PHYSDEV: physical device associated with the vlan device.
        * BONDING_OPTS: Bonding parameters of the Bond device.
        * BONDING_MASTER: 'yes' if its bond device.
        * SLAVES: Returns slaves associated with the bond.
        * NETTYPE(system z): Returns network device driver type
        * SUBCHANNELS(system z):List of sub channels(network triplets) of
                                the interface
    * IPV4_INFO:IPV4 information of network interface:
        * IPV4INIT : IPV4 initialization indicator
        * BOOTPROTO: Boot protocol of ipv4
        * DEFROUTE: indicates default route value
        * DNSAddresses: Lists DNS ipv4 addresses
        * IPV4Addresses: single or multiple ipv4 address of interface
            * IPADDR: ipv4 address of the interface
            * PREFIX: Prefix of the ipv4 address
            * GATEWAY: Gateway assigned to the ipv4 address
        * ROUTES: Assign single or multiple routes to interface
                * ADDRESS: ipv4 address of the interface
                * PREFIX: prefix of the ipv4 address
                * GATEWAY: Gateway assigned to the ipv4 address
		        * METRIC: Cost values used by the router
    * IPV6_INFO:IPV6 information of network interface:
        * IPV6INIT: initalize indicator for ipv6 for the interface
        * IPV6_AUTOCONF: automatic mode of ipv6
        * IPV6_DEFROUTE: Use default route
        * IPV6_DEFAULTGW: Gateway assigned to the ipv6 address
        * DNSAddresses: List of DNS ipv6 addresses
        * IPV6Addresses:single or multiple ipv6 address to interface
            * IPADDR:  address of the interface
            * PREFIX: Prefix of the address
        * ROUTES: Assign routes to interface
            * ADDRESS: ipv6 address of the interface
            * NETMASK: netmask of the ipv6 address
            * GATEWAY: Gateway assigned to the ipv6 address
		    * METRIC: Cost values used by the router

* **PUT**: update the parameters in network interface file
           /etc/sysconfig/network-scripts/ifcfg-<name>
    * BASIC_INFO: Dictionary containing the basic information of interface
                  to be updated
        * NAME *(optional)*: Name of the interface.
        * ONBOOT *(optional)*: 'Yes' if interface is to be brought up during boot,
                                'No' if interface should not be brought up during boot.
        * MTU *(optional)*: Maximum Transmission Unit
        * ZONE *(optional)*: Firewall Zone for the interface
    * IPV4_INFO *(optional)*: Dictionary containing the ipv4 information of
    interface to be created
        * IPV4INIT : Yes, initialize ipv4.
        * BOOTPROTO: Boot protocol for ipv4(dhcp,none,autoip)
        * DEFROUTE(for BOOTPROTO none or dhcp) *(optional)*: 'yes' Use
        default route.
        * IPV4Addresses(Needed if BootProto is none): Assign single or
        multiple ipv4 address to interface
            * IPADDR: ipv4 address of the interface
            * NETMASK: netmask of the ipv4 address
            * GATEWAY *(optional)*: Gateway assigned to the ipv4 address
        * DNSAddresses *(optional)*: List of DNS ipv4 addresses
        * ROUTES *(optional)*: Assign single or multiple routes to interface
                * ADDRESS: ipv4 address of the interface
                * NETMASK: netmask of the ipv4 address
                * GATEWAY: Gateway assigned to the ipv4 address
		        * METRIC *(optional)*: Cost values used by the router
    * IPV6_INFO *(optional)*: Dictionary containing the ipv6 information of
    interface to be updated
        * IPV6INIT: 'yes' to initalize ipv6 for the interface
        * IPV6_AUTOCONF: 'yes' automatic mode for ipv6,''no' for other mode
        * DHCPV6C: 'yes' dhcp automatic mode for ipv6
        * IPV6_DEFROUTE *(optional)*: 'yes' Use default route.
        * IPV6Addresses(Needed if IPV6_AUTOCONF is no):
                         Assign single or multiple ipv6 address to interface
            * IPADDR:  address of the interface
            * NETMASK: netmask of the address
        * DNSAddresses *(optional)*: List of DNS ipv6 addresses stored as
                                     DNS1,DNS2
        * IPV6_PEERDNS *(optional)*: 'yes' use the peerdns configured
        * IPV6_PEERROUTES *(optional)*: 'yes' use PEERROUTES
        * IPV6_DEFAULTGW *(optional)*: Gateway assigned to the ipv6 address
        * ROUTES *(optional)*: Assign routes to interface
                * ADDRESS: ipv6 address of the interface
                * NETMASK: netmask of the ipv6 address
                * GATEWAY: Gateway assigned to the ipv6 address
		        * METRIC *(optional)*: Cost values used by the router

* **POST**: Create an interface of types default interface, bond and vlan
    * BASIC_INFO: Dictionary containing the basic information of interface
    to be created
        * DEVICE: Device name of the interface.
        * NAME *(optional): Name of the interface.
        * ONBOOT *(optional)*:
                        'Yes' if interface is to be brought up during boot
                        'No' if interface should not be brought up during boot.
        * MTU *(optional)*: Maximum Transmission Unit
        * ZONE *(optional)*: Firewall Zone for the interface
        * BOND_INFO *(Needed if TYPE is bond)*: Dictionary containing the bond information
         of interface to be created
            * BONDING_MASTER *: 'yes' indicates that the device is a bonding
             master device.  The only useful value is "yes."
            * SLAVES *: List of slave interfaces
            * BONDING_OPTS *(OPTIONAL)*: Dictionary of bonding options for
            the keys
                * ad_select *(OPTIONAL)*: value
                    Possible values are: stable or 0, bandwidth or 1, count
                    or 2
                * arp_interval *(OPTIONAL)*: time_in_milliseconds
                * arp_ip_target *(OPTIONAL)*:
                    Possible values are:
                        ip_address[,ip_address_2,... ip_address_16]
                        Up to 16 IP addresses can be specified in a comma
                        separated list
                * arp_validate *(OPTIONAL)*: value
                    Possible values are: none or 0, active or 1, backup or
                    2, all or 3, filter or 4, filter_active or 5,
                    filter_backup or 6, downdelay= time_in_milliseconds
                * fail_over_mac= value *(OPTIONAL)*: value
                    Possible values are: none or 0, active or 1, follow or 2
                * lacp_rate *(OPTIONAL)*: value
                    Possible values are: slow or 0, fast or 1
                * miimon *(OPTIONAL)*: time_in_milliseconds
                * mode *(OPTIONAL)*: value
                    Possible values are: balance-rr or 0, active-backup or
                    1, balance-xo r or 2, broadcast or 3, 802.3ad or 4,
                    balance-tlb or 5, balance-alb or 6
                * primary *(OPTIONAL)*: interface_name
                * primary_reselect *(OPTIONAL)*: value
                    Possible values are: always or 0, better or 1, failure or 2
                * resend_igmp *(OPTIONAL)*: value
                    The valid range is 0 to 255
                * updelay *(OPTIONAL)*: time_in_milliseconds
                * use_carrier *(OPTIONAL)*: number
                    Possible values are: 0, 1
                * xmit_hash_policy *(OPTIONAL)*: value
                    Possible values are: layer2, layer2+3, layer3+4,
                    encap2+3, encap3+4
        * VLAN_INFO *(Needed if TYPE is Vlan)*: Dictionary containing the vlan information
         of interface to be created
            * PHYSDEV *: A previously configured interface can be selected.
            * VLAN *: 'yes'
            * VLANID *: The identification number to be used to tag the VLAN
             network traffic.
        * TYPE *: Type of an interface
                Example: Ethernet, Bond, Vlan
    * IPV4_INFO *(optional)*: Dictionary containing the ipv4 information of
            interface to be created
        * IPV4INIT : Yes, initialize ipv4.
        * BOOTPROTO: Boot protocol for ipv4(dhcp,none,autoip)
        * DEFROUTE(for BOOTPROTO none or dhcp) *(optional)*: 'yes' Use
        default route.
        * IPV4Addresses(Needed if BootProto is none): Assign single or
        multiple ipv4 address to interface
            * IPADDR: ipv4 address of the interface
            * NETMASK: netmask of the ipv4 address
            * GATEWAY *(optional)*: Gateway assigned to the ipv4 address
        * DNSAddresses *(optional)*: List of DNS ipv4 addresses
        * ROUTES *(optional)*: Assign single or multiple routes to interface
                * ADDRESS: ipv4 address of the interface
                * NETMASK: netmask of the ipv4 address
                * GATEWAY: Gateway assigned to the ipv4 address
		        * METRIC *(optional)*: Cost values used by the router
    * IPV6_INFO *(optional)*: Dictionary containing the ipv6 information of
            interface to be updated
        * IPV6INIT: 'yes' to initalize ipv6 for the interface
        * IPV6_AUTOCONF: 'yes' automatic mode for ipv6,''no' for other mode
        * DHCPV6C: 'yes' dhcp automatic mode for ipv6
        * IPV6_DEFROUTE *(optional)*: 'yes' Use default route.
        * IPV6Addresses(Needed if IPV6_AUTOCONF is none and DHCPV6C is no ):
                         Assign single or multiple ipv6 address to interface
            * IPADDR:  address of the interface
            * NETMASK: netmask of the address
        * DNSAddresses *(optional)*: List of DNS ipv6 addresses stored as
                                     DNS1,DNS2
        * IPV6_PEERDNS *(optional)*: 'yes' use the peerdns configured
        * IPV6_PEERROUTES *(optional)*: 'yes' use PEERROUTES
        * IPV6_DEFAULTGW *(optional)*: Gateway assigned to the ipv6 address
        * ROUTES *(optional)*: Assign routes to interface
                * ADDRESS: ipv6 address of the interface
                * NETMASK: netmask of the ipv6 address
                * GATEWAY: Gateway assigned to the ipv6 address
		        * METRIC *(optional)*: Cost values used by the router


* **DELETE**: Delete an interface of types bond and vlan

### Collection: Swap devices**

**URI:** /plugins/ginger/swaps

**Methods:**

* **GET**: Retrieve a summarized list of all swap devices
* **POST**: Create a swap device
   *type : Type could be either `device` or `file`.
   *size : Only applicable if the swap device type is `file`.
   *file_loc : Absolute path of the device.

### Resource: Swap Device**

**URI:** /plugins/ginger/swaps/*:device_name*

**Methods:**

* **GET**: Retrieve the full description of a Swap Device

   *filename : File name of the Swap Device
   *type : The type of the Swap Device. `partition` for the block device and `file` for the regular file.
   *size : Size of the Swap Device
   *used : Amount of Swap Device space used
   *priority : Priority of the Swap Device

* **DELETE**: Remove the Swap Device

### Collection: DASD Devices

URI: /plugins/ginger/dasddevs

**Methods:**

* **GET**: Retrieve a detailed list of all DASD devices

* **POST**: Format a DASD device
        * blk_size: Block size to be used for formatting a DASD device.

### Resource: DASD Device

URI: /plugins/ginger/dasddevs/*:bus_id*

**Methods:**

* **GET**: Retrieve the description of a single DASD device

        * status: Status of the DASD device:
        * active: dasd device is in active state
        * blocks: Number of blocks.
        * name:  Name of DASD device.
        * uid: uid of DASD device.
        * type: Device type.
        * eer_enabled: Indicates whether the DASD is enabled for extended error reporting
                        ('1' if enabled and '0' if it is not enabled).
        * erplog: Indicates whether error recovery processing (ERP) logging is enabled
                        ('1' if enabled and '0' if it is not enabled).
        * use_diag: Indicates whether the DIAG access method is enabled
                        ('1' if enabled and '0' if it is not enabled).
        * readonly: '1' if the DASD is read-only, '0' if it can be written to.
        * device: '1' if the DASD is read-only, '0' if it can be written to.
        * blksz: Block size used for formatting DASD device.
        * bus_id: Bus id of the DASD device.
        * size: Size of DASD device in MB.

### Collection: DASD Partitions

URI: /plugins/ginger/dasdpartitions

**Methods:**

* **GET**: Retrieve a detailed list of all DASD Partitions of the host

* **POST**: Create a DASD Partition
        * dev_name: Name of DASD device.
        * size: Size of the partition to be created.

### Resource: DASD Partition

URI: /plugins/ginger/dasdpartitions/*:name*

**Methods:**

* **GET**: Retrieve the description of a single DASD Partition

        * name: Name of the dasd partition.
        * fstype: The file system type of the partition.
    * path: Path of the partition.
        * mountpoint: If the partition is mounted, represents the mountpoint.
      Otherwise blank.
        * type: The type of the partition.
        * size:  Total size of the partition, in bytes.
        * available: false, if the partition is in use by system; true, otherwise.

* **DELETE**: Delete the DASD Partition

### Collection: Partitions

URI: /plugins/ginger/partitions

**Methods:**

* **GET**: Retrieve a summarized list of all partitions and disks

* **POST**: Create a partition
     * devname : Path of the device to be partitioned.
     * partsize : Size of the partition

### Resource: Partition

URI: /plugins/ginger/partitions/*:part_name*

**Methods:**

* **GET**: Retrieve the full description of the partition or disk

     * name: Name of the partition or disk
     * fstype: Type of the filesystem on the partition or disk
     * path:  Path of the partition or disk
     * mountpoint: Mount point of the partition or disk
     * type : Type of the device. `part` for partition, `disk` for disk and `mpath` for multipath devices
     * size : Size of the partition or disk

* **DELETE**: Delete the partition

**Actions (POST):**
  * change_type: Change the type of the partition
    * type: Hex value of the new type (e.g 82 for swap type)
  * format: Format the partition with the specified filesystem type
    * fstype: type of the filesystem (e.g ext3)

### Collection: Physical Volumes

**URI:** /plugins/ginger/pvs

**Methods:**

* **GET**: Retrieve a summarized list of all physical volumes
* **POST**: Create a physical volume
   * pv_name : Path of the device to be used as a physical volume

### Resource: Physical Volume

**URI:** /plugins/ginger/pvs/*:pvname*

**Methods:**

* **GET**: Retrieve the full description of a Physical Volume

   * PVName : Path of the physical volume.
   * VGName : Name of the volume group to which the physical volume belongs.
   * PVSize : Size of the physical volume.
   * Allocatable : Specifies if the volume is allocatable.
   * PESize : Size of each physical extent.
   * TotalPE: Total physical extents on the volume.
   * FreePE: Number of free physical extents.
   * AllocatedPE : Number of allocated physical extents.
   * PVUUID : UUID of the physical volume.

* **DELETE**: Remove the Physical Volume.

### Collection: Volume Groups

**URI:** /plugins/ginger/vgs

**Methods:**

* **GET**: Retrieve a summarized list of all volume groups
* **POST**: Create a volume group
   * vg_name : Name of a volume group
   * pv_paths : Paths of the physical volumes to be added to the volume group

### Resource: Volume Groups

**URI:** /plugins/ginger/vgs/*:vgname*

**Methods:**

* **GET**: Retrieve the full description of a volume group

   * vgName : Name of the volume group.
   * vgStatus : `extendable` if the VG is extendable.
   * vgSize : Size of the volume group.
   * maxLV : Maximum number of LVs allowed in VG or 0 if unlimited.
   * freePESize : Size of free PE.
   * format: Type of metadata.
   * curLV: Number of LVs.
   * metadataAreas : Number of metadata areas on this VG.
   * permission : VG permissions.
   * allocPE : Number of allocated PEs.
   * pvNames : List of PVs in the VG.
   * peSize : Size of each PE.
   * systemID : System ID.
   * curPV : Number of PVs.
   * freePE : Amount of free PEs.
   * maxPV : Maximum number of PVs allowed in VG or 0 if unlimited.
   * totalPE : Total number of Physical Extents.
   * vgUUID : UUID of the volume group.
   * allocPESize : Size of allocated PE.
   * metadataSequenceNo : Revision number of internal metadata.

* **DELETE**: Remove the Volume Group.

**Actions (POST):**
  * extend: Extend the volume group with additional PVs.
    * pv_paths: List of PV paths to be added to the VG.
  * reduce: Reduce the volume group by removing PVs.
    * pv_paths: List of PV paths to be added to the VG.

### Collection: Logical Volumes

**URI:** /plugins/ginger/lvs

**Methods:**

* **GET**: Retrieve a summarized list of all logical volumes
* **POST**: Create a logical volume
   * vg_name : Name of the volume group required to create the logical volume
   * size : Size of the logical volume

### Resource: Logical Volume

**URI:** /plugins/ginger/lvs/*:lvpath*

**Methods:**

* **GET**: Retrieve the full description of a Logical Volume

   * lvName : Name of the logical volume.
   * vgName : Name of the volume group.
   * lvPath : Path of the logical volume.
   * segments : Number of segments in LV.
   * #open : open count of LV.
   * blockDevice : Maj:Min number of the LV.
   * lvStatus : State of the LV.
   * lvCreationhost, time : Details of the host creating the LV, time stamp of creating LV.
   * -currentlySetTo : Internal logical volume number.
   * allocation : Allocation policy of the LV.
   * lvUUID : UUID of the LV.
   * currentLE : Current logical extents associated with the LV.
   * lvWriteAccess : Logical volume access.
   * lvSize : Size of the LV.
   * readAheadSectors : Read ahead sectors of LV.

  Additional fields if LV contains snapshot:
	* lvSnapshotStatus : Status of the snapshot.
	* COW-tableLE : logical extents associated with COW-table.
	* COW-tableSize : Size of COW-table.
	* snapshotChunkSize : Size of each unit of data in snapshot.

* **DELETE**: Remove the Logical Volume.

### SimpleCollection: List of storage devices

**URI:** /plugins/ginger/stgdevs

**Methods:**

* **GET**: Retrieve a summarized list of all storage devices

### Collection: Interfaces

**URI:** /plugins/ginger/network/interfaces

**Methods:**

* **GET**: Retrieve a detailed list of interfaces

### Resource: Interfaces

**URI:** /plugins/ginger/network/interfaces/*:interfacename*

**Methods:**

* **GET**: Retrieve the full description of a interface
    * status: The current physical link state of the interface.
    * name: Interface name
    * editable: 'true' if interface can be edited, 'false' otherwise
    * ipaddr: IP address currently assigned to this interface
    * netmask: Netmaks of interface
    * type: Type of interface
     Example: Bond, Vlan, Ethernet etc

* **POST**:
   * activate : Activates an interface
   * deactivate : Deactivates an interface

### Collection: SysModules

URI: /plugins/ginger/sysmodules

**Methods:**

* **GET**: Retrieve a list of all loaded kernel modules (lsmod output).
* Returns: a list of SysModule objects.

* **POST**: Load a kernel module using modprobe.
        * module: the name of the module.
        * parms: arguments to be passed to the module, as you would with modprobe.
* Returns: the full description of the module loaded.

### Resource: SysModule

URI: /plugins/ginger/sysmodules/*:module_name*

*Methods:**

* **GET**: Retrieve the full description of the module. Note that you can retrieve information
of all available modules, not just the loaded ones. At this moment there is no attribute that will indicate whether a module is loaded or not. The following fields can somethings be ommited, so the caller must verify the existence of each one but 'name' and 'filename':
        * name - string
        * filename - string
        * description - string
        * authors  -array
        * depends - array
        * intree - str
        * license - str
        * vermagic - str
        * signer -str
        * sig_key - str
        * sig_hashalgo -str
        * aliases - an array of alias.
        * parms - a dictionary of parm (module parameters) with format {param_name1: param_desc1, param_name2: param_desc2 ...}
        * features - a dictionary that describes feature enablement given certain parameters of the module, for example SR-IOV in some Ethernet cards. This dictionary has the format {feature1: {desc: description_of_feature1, parms: array_of_parm_that_enables_feature1}, feature2:{...} ...}
* Returns: a dictionary with the fetched values.

* **DELETE**: Unload a loaded kernel module using modprobe -r.
* Returns: nothing.

### Collection: Users

**URI:** /plugins/ginger/users

**Methods:**

* **GET**: Retrieve the list of users of the current host
    * profile: user role in Wok (kimchiuser, virtuser, admin)
    * gid: group user id
    * uid: user id
    * group: group name
    * name: user name

* **POST**: Create a new user
    * profile: user role in Wok:
        * kimchiuser: user with no admin rights, disabled login
        * admin: user with admin rights (added to sudoers)
        * virtuser: user added to kvm group
    * name: user name
    * password: user password
    * group: user group

### Resource: User

**URI:** /plugins/ginger/users/*:name*

**Methods**

* **DELETE**: delete the given user
