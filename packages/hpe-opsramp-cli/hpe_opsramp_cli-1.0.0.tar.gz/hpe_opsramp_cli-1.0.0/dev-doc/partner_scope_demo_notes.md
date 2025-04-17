# Demo objective
Show state transition and *managed by* tag to unmanaged devices upon third party alerts
unmanage alert resources at  partner scope

# Demo environment 
## UAT
### Partner 
National INC : ed0d8f51-e7f3-40cc-b117-63847a3cc9cc

### Clients
1) ITC client : 649c8df6-569e-4aab-8b1d-c132290b602c
these two are not unmanged keep them active before demo
nextgen-gw   : 6f4bf447-072f-494e-bdc1-d4aa42e6b382
00505698B541 : 65443f03-6c07-4be9-a69f-6a898c1dcd90

testdevice-api4 : ec0115f5-594b-4a36-b2a8-1717938365ae
testdevice-api5 : f2d9defb-8aa4-4d18-90c8-8f9f590efe76
testdevice-api6 : bf37666b-b08d-4c28-af08-91f1d09bd513
testdevice-api53 : 422e63a3-538b-42ac-87d8-2152e58e84a9

2) BalaSubramanian-API : cc0c2a2e-9c63-46b5-9db2-ec9f6d7dbcbd
   API Alerts 1 : d92c999d-eace-4502-884f-4ac8799dfc08
   API Alerts 2 : 93a90c21-bd56-4674-9790-801b38c51e95
   API Alerts 3 : 5d4cac04-a8b0-4a73-bfb4-d1db9e8a7867
   API Alerts 4 : d47807a1-71da-4c79-b8ef-643cc581501c
3) ITC Client 1 : ac7a96d4-8ab1-4c87-baf8-98706df1f58c
   



# Prerequiste
unmanaged devices on more than one client of partner
open UAT https://uat.opsramp.net/portal/infra-ui/resources

## vs code
cd C:\Users\vetrivel\namasivaya\opsrampcli
.\.venv\Scripts\Activate.ps1

# Demo steps
## show unmanaged devices across partner i.e. more than one clients
view : unmanaged devices of National INC
OpsQL : state = "inactive" AND clientName IN ("balasubramanian-api","itc client 1")

## Show 0 alerts browser before post alerts to unmanaged devices 
view: last 10 mintues
OpsQL: createdTime > "-10min" clientName IN ("balasubramanian-api","itc client 1")

## - Third-party alerts on unmanaged resources
### post alerts on UAT_BalaSubramanian_API
opcli postalerts --env UAT_BalaSubramanian_API --infile .\create-alerts-UAT-3-devices-input.json

### post alerts on ITC client
 opcli postalerts --env UAT_ITC_Client --infile .\create-alerts-UAT-ITCClient-3-devices-input.json
 
 show resources individual page with tags and tag values 
- show unmange old UI 

## Appendix 
### test results on UAT_National_INC - 
opsramp-cli unmanage_alert_resources --env UAT_National_INC        
[05:57:55] Found 10 alert only resources ...                                                                                                       cli_utils.py:257Finding out alert only resources ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
           Starting to unmanage alert only resources of 3 clients ...                                                                              cli_utils.py:144           Unmanaging 2 alert only resources of client : 649c8df6-569e-4aab-8b1d-c132290b602c ...                                                  cli_utils.py:200[06:02:57] Unmanaging 4 alert only resources of client : cc0c2a2e-9c63-46b5-9db2-ec9f6d7dbcbd ...                                                  cli_utils.py:200[06:03:02] Unmanaging 4 alert only resources of client : b1838501-9d66-4c09-99e0-7db0b8812a7e ...                                                  cli_utils.py:200Unmanaging alert only resources ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
(hpe-opsramp-cli) PS C:\Users\vetrivel\src\GitHub-HPE-OpsRamp-CLI\hpe-opsramp-cli> 

## POD7 details
## Demo environment 
POD 7 - Open issue tags are not getting applied.ITOM-97719 Alert posted on unmanged device not applying Managed by tag on POD7
Partner
GLP - HPE Flex Metering Project : d06a517e-17dc-43fb-b482-c9ed78ab6f68
CLients
API Showcase   : b2ddde6f-327a-49e7-b63b-11f818c662ea
API Showcase 2 : 32b50e46-6ef8-4cb6-9902-400dca670304

# Demo steps
## show unmanaged devices across partner i.e. more than one clients
view : API showcase all devices
OpsQL : clientName IN ("api showcase","api showcase 2")

view : API showcase all devices
OpsQL : clientName IN ("api showcase","api showcase 2") AND state = "inactive" 

## Show alerts browser before post alerts to unmanaged devices 
view: last 10 mintues
OpsQL: clientName IN ("API Showcase","API Showcase2") AND createdTime < "-10m"

## - Third-party alerts on unmanaged resources
### post alerts on API showcase
opcli postalerts --env POD7_GLP_Flex_Partner --infile .\create-alerts-POD7-3-devices-input.json

 show resources individual page with tags and tag values 
- show unmange old UI 
