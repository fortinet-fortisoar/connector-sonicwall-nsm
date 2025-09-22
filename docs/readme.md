## About the connector
SonicWall Network Security Manager (NSM) is a cloud-based (or on-prem) platform designed to centrally manage, monitor, and report on SonicWall firewalls and security policies across distributed environments.
<p>This document provides information about the SonicWall NSM Connector, which facilitates automated interactions, with a SonicWall NSM server using FortiSOAR&trade; playbooks. Add the SonicWall NSM Connector as a step in FortiSOAR&trade; playbooks and perform automated operations with SonicWall NSM.</p>

### Version information

Connector Version: 1.0.1


Authored By: Fortinet

Certified: No

### Release Notes for version 1.0.1

#### The following enhancements have been made to the SonicWall NSM Connector in version 1.0.1:

- Fixed an issue where the health check was failing to connect to the SonicWall NSM server.

## Installing the connector
<p>From FortiSOAR&trade; 6.0.0 onwards, use the <strong>Connector Store</strong> to install the connector. For the detailed procedure to install a connector, click <a href="https://docs.fortinet.com/document/fortisoar/0.0.0/installing-a-connector/1/installing-a-connector" target="_top">here</a>.<br>You can also use the following <code>yum</code> command as a root user to install connectors from an SSH session:</p>
`yum install cyops-connector-sonicwall-nsm`

## Prerequisites to configuring the connector
- You must have the URL of SonicWall NSM server to which you will connect and perform automated operations and credentials to access that server.
- The FortiSOAR&trade; server should have outbound connectivity to port 443 on the SonicWall NSM server.

## Minimum Permissions Required
- N/A

## Configuring the connector
For the procedure to configure a connector, click [here](https://docs.fortinet.com/document/fortisoar/0.0.0/configuring-a-connector/1/configuring-a-connector)
### Configuration parameters
<p>In FortiSOAR&trade;, on the Connectors page, click the <strong>SonicWall NSM</strong> connector row (if you are in the <strong>Grid</strong> view on the Connectors page) and in the <strong>Configurations&nbsp;</strong> tab enter the required configuration details:&nbsp;</p>
<table border=1><thead><tr><th>Parameter<br></th><th>Description<br></th></tr></thead><tbody><tr><td>Server URL<br></td><td>Specify the server URL of the SonicWall NSM server to connect and perform automated operations.<br>
<tr><td>API Key<br></td><td>Specify the API Key to connect to the endpoint and perform automated operations.<br>
<tr><td>Verify SSL<br></td><td>Specifies whether the SSL certificate for the server is to be verified or not. <br/>By default, this option is set as True.<br></td></tr>
</tbody></table>

## Actions supported by the connector
The following automated operations can be included in playbooks and you can also use the annotations to access operations from FortiSOAR&trade; release 4.10.0 and onwards:
<table border=1><thead><tr><th>Function<br></th><th>Description<br></th><th>Annotation and Category<br></th></tr></thead><tbody><tr><td>Get Access Rules<br></td><td>Retrieve the list of access rules between the from and to zones from SonicWall NSM.<br></td><td>get_access_rules <br/>Investigation<br></td></tr>
<tr><td>Create Address Object<br></td><td>Update an existing address object on a SonicWall NSM server based on the parameters you have specified.<br></td><td>create_address_object <br/>Investigation<br></td></tr>
<tr><td>Get Address Object<br></td><td>Retrieve the list of connected items to address objects within the SonicWall NSM server.<br></td><td>get_address_objects <br/>Investigation<br></td></tr>
<tr><td>Update Address Object<br></td><td>Add a address object on a SonicWall NSM server based on the parameters you have specified.<br></td><td>update_address_object <br/>Investigation<br></td></tr>
<tr><td>Execute an API Request<br></td><td>Sends an API request to an API endpoint based on specified HTTP method, endpoint, and other input parameters that you have specified, enabling flexible API interactions tailored to user needs.<br></td><td>execute_an_api_call <br/>Investigation<br></td></tr>
</tbody></table>

### operation: Get Access Rules
#### Input parameters
<table border=1><thead><tr><th>Parameter<br></th><th>Description<br></th></tr></thead><tbody><tr><td>Filter Type<br></td><td>Select the filter type to retrieve access rules. You can choose from the following options: From Zone to To Zone, Source Address to Destination Address, or Source Port to Destination Port<br>
<strong>If you choose 'Source Zone to Destination Zone'</strong><ul><li>Source Zone: Specify the source zone to filter access rules. Note: If you specify "Any" all values need to be considered.</li><li>Destination Zone: Specify the destination zone to filter access rules. Note: If you specify "Any" all values need to be considered.</li></ul><strong>If you choose 'Source Address to Destination Address'</strong><ul><li>From Address: Specify the source address to filter access rules. If you are using address object names, they must exist in the firewall configuration. Note: If you specify "Any", all values will be considered.</li><li>Destination Address: Specify the destination address to filter access rules. If you are using address object names, they must exist in the firewall configuration. Note: If you specify "Any", all values will be considered.</li></ul><strong>If you choose 'Source Port to Destination Port'</strong><ul><li>Source Port: Specify the source port to filter access rules. Note: If you specify "Any" all values need to be considered.</li><li>Destination Port: Specify the destination port to filter access rules. Note: If you specify "Any" all values need to be considered.</li></ul></td></tr><tr><td>Device Serial Number<br></td><td>Specify the device serial number to filter access rules.<br>
</td></tr><tr><td>Rule Type<br></td><td>Select the rule type to retrieve access rules. You can choose from the following options: Access Rules or Security Policies. By default, it set as "Access Rules"<br>
</td></tr><tr><td>Limit<br></td><td>If a specific number of child relationships is required, check the limit option. To retrieve all values, leave the option unchecked.<br>
</td></tr><tr><td>Limit Total Count<br></td><td>Specifies the limitCount value is used to determine how many child relationships are required. This parameter helps control the volume of data by limiting the total count of items in the response.<br>
</td></tr><tr><td>Children Object Types<br></td><td>Specify the children object type to filter access rules.<br>
</td></tr></tbody></table>

#### Output

 The output contains a non-dictionary value.
### operation: Create Address Object
#### Input parameters
<table border=1><thead><tr><th>Parameter<br></th><th>Description<br></th></tr></thead><tbody><tr><td>Address Object Name<br></td><td>Specify the name for the address object you want to update.<br>
</td></tr><tr><td>Zone<br></td><td>Specify the security zone that the address object belongs to on the SonicWall NSM server.<br>
</td></tr><tr><td>Object Type<br></td><td>Select the object type to update the address object in SonicWall NSM server. You can choose from the following options: Host (Single IP Address), Network (IP/Subnet), Range (Start IP - End IP), FQDN (Domain Name), or MAC Address.<br>
<strong>If you choose 'Host (Single IP Address)'</strong><ul><li>IP Address: Specify the specific IP address of the host to be added as an address object.</li></ul><strong>If you choose 'Network (IP/Subnet)'</strong><ul><li>IP Address: Specify the base IP address of the network to be used for this address object.</li><li>Netmask: Specify the subnet mask associated with the network address.</li></ul><strong>If you choose 'Range (Start IP - End IP)'</strong><ul><li>Starting Range of IP Address: Specify the starting IP address of the range.</li><li>Ending Range of IP Address: Specify the ending IP address of the range.</li></ul><strong>If you choose 'FQDN (Domain Name)'</strong><ul><li>Fully Qualified Domain Name (FQDN): Specify the DNS-resolvable domain name used to create this address object.</li></ul><strong>If you choose 'MAC Address'</strong><ul><li>MAC Address: Specify the physical (MAC) address of the device to associate with this object.</li></ul></td></tr><tr><td>Description<br></td><td>Specify the description for the address object you want to create.<br>
</td></tr><tr><td>Device Serial Number<br></td><td>Specify the device serial number to create the address object.<br>
</td></tr></tbody></table>

#### Output

 The output contains a non-dictionary value.
### operation: Get Address Object
#### Input parameters
<table border=1><thead><tr><th>Parameter<br></th><th>Description<br></th></tr></thead><tbody><tr><td>Address Object Name/UUID<br></td><td>Specify the name or UUID for the address object based on which you want to retrieve connected items.<br>
</td></tr><tr><td>Is UUID<br></td><td>Uncheck this option if you are passing a address object name instead of a address object UUID.<br>
</td></tr><tr><td>Device Serial Number<br></td><td>Specify the device serial number to retrieve the address object.<br>
</td></tr></tbody></table>

#### Output

 The output contains a non-dictionary value.
### operation: Update Address Object
#### Input parameters
<table border=1><thead><tr><th>Parameter<br></th><th>Description<br></th></tr></thead><tbody><tr><td>Address Object UUID<br></td><td>Specify the UUID for the address object you want to update.<br>
</td></tr><tr><td>Address Object Name<br></td><td>Specify the name for the address object you want to update.<br>
</td></tr><tr><td>Zone<br></td><td>Specify the security zone that the address object belongs to on the SonicWall NSM server.<br>
</td></tr><tr><td>Object Type<br></td><td>Select the object type to create the address object in SonicWall NSM server. You can choose from the following options: Host (Single IP Address), Network (IP/Subnet), Range (Start IP - End IP), FQDN (Domain Name), or MAC Address.<br>
<strong>If you choose 'Host (Single IP Address)'</strong><ul><li>IP Address: Specify the IP address representing the host you want to update in the address object.</li></ul><strong>If you choose 'Network (IP/Subnet)'</strong><ul><li>IP Address: Specify the base IP address of the network to update the network address object.</li><li>Netmask: Specify the subnet mask to update the range of the network in the address object.</li></ul><strong>If you choose 'Range (Start IP - End IP)'</strong><ul><li>Starting Range of IP Address: Specify the starting IP address you want to update for the range address object.</li><li>Ending Range of IP Address: Specify the ending IP address you want to update for the range address object.</li></ul><strong>If you choose 'FQDN (Domain Name)'</strong><ul><li>Fully Qualified Domain Name (FQDN): Specify the fully qualified domain name (FQDN) you want to update in the address object.</li></ul><strong>If you choose 'MAC Address'</strong><ul><li>MAC Address: Specify the physical MAC address you want to update in the address object.</li></ul></td></tr><tr><td>New Address Object Name<br></td><td>Specify the new name for the address object you want to update in SonicWall NSM server.<br>
</td></tr><tr><td>Device Serial Number<br></td><td>Specify the device serial number to update the address object.<br>
</td></tr></tbody></table>

#### Output

 The output contains a non-dictionary value.
### operation: Execute an API Request
#### Input parameters
<table border=1><thead><tr><th>Parameter<br></th><th>Description<br></th></tr></thead><tbody><tr><td>HTTP Method<br></td><td>Select an HTTP action for the request. You can select from the following options:  

DELETE 

GET 

PATCH 

POST 

PUT <br>
</td></tr><tr><td>Endpoint<br></td><td>Specify the target API URL path for the request. For example, if the website is https://example.com and URL path is https://example.com/images/pic.jpg, the endpoint would be images/pic.jpg.<br>
</td></tr><tr><td>Query Parameters<br></td><td>(Optional) Specify any optional parameters to add to the URL and refine the request.<br>
</td></tr><tr><td>Request Payload<br></td><td>(Optional) Specify data, as JSON, to be sent as the request payload (typically for POST or PUT requests).<br>
</td></tr></tbody></table>

#### Output

 The output contains a non-dictionary value.
## Included playbooks
The `Sample - SonicWall NSM - 1.0.1` playbook collection comes bundled with the SonicWall NSM connector. These playbooks contain steps using which you can perform all supported actions. You can see bundled playbooks in the **Automation** > **Playbooks** section in FortiSOAR<sup>TM</sup> after importing the SonicWall NSM connector.

- Get Access Rules
- Create Address Object
- Get Address Object
- Update Address Object
- Execute an API Request

**Note**: If you are planning to use any of the sample playbooks in your environment, ensure that you clone those playbooks and move them to a different collection, since the sample playbook collection gets deleted during connector upgrade and delete.
