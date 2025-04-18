from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

class Sonar:
    def __init__(self, sonar_url, token):
        self.client = Client(
            transport=RequestsHTTPTransport(
                url=sonar_url,
                headers={
                    'Authorization': 'Bearer ' + token
                }
            )
        )

    def graphql(self, query, variables=None):
        return self.client.execute(gql(query), variable_values=variables)


    def getAccounts(self, id=None, qty=None):
        if id and qty == None:
            inputs = ""
        elif id != None and qty == None:
            inputs = f"""(id:{id})"""
        elif id == None and qty != None:
            input = f"""(paginator:{{page:1, records_per_page:{qty}}})"""
        elif id != None and qty !=None:
            input = f"""(id:{id}, paginator:{{page:1, records_per_page:{qty}}})"""
        query = f"""{{
                    accounts{input}{{
                        entities {{
                        id
                        name
                        account_status {{
                            id
                            activates_account
                        }}
                        account_services {{
                            entities {{
                            id
                            service {{
                                id
                                name
                                type
                                amount
                                data_service_detail {{
                                upload_speed_kilobits_per_second
                                download_speed_kilobits_per_second
                                }}
                            }}
                            }}
                        }}
                        addresses {{
                            entities {{
                            id
                            inventory_items {{
                                entities {{
                                inventory_model {{
                                    id
                                    name
                                    manufacturer {{
                                    id
                                    name
                                    }}
                                }}
                                inventory_model_field_data {{
                                    entities {{
                                    value
                                    ip_assignments {{
                                        entities {{
                                        subnet_id
                                        subnet
                                        }}
                                    }}
                                    inventory_model_field {{
                                        id
                                        name
                                    }}
                                    }}
                                }}
                                }}
                            }}
                            }}
                        }}
                        }}
                    }}
                    }}"""
        
        return self.graphql(query, None)['accounts']['entities']
    

    def getAccountServices(self):
        query = """{
                    account_services(paginator:{page:1, records_per_page:1000000}){
                        entities{
                        service{
                            name
                            id
                            type
                            amount
                            enabled
                            company_id
                            data_service_detail{
                            download_speed_kilobits_per_second
                            upload_speed_kilobits_per_second
                            }
                        }
                        }
                    }
                    }"""
        
        return self.graphql(query, None)['account_services']['entities']


    def getAddressLists(self):
        query = """{
                    address_lists(paginator:{page:1, records_per_page:1000000}){
                        entities{
                        id
                        name
                        account_statuses{
                            entities{
                            id
                            name
                            }
                        }
                        services{
                            entities{
                            id
                            name
                            }
                        }
                        }
                    }
                    }"""
        
        return self.graphql(query, None)['address_lists']['entities']
    

    def getAccountStatuses(self):
        query = """{
                    account_statuses(paginator:{page:1, records_per_page:1000000}){
                        entities{
                        id
                        name
                        activates_account
                        }
                    }
                    }"""
        
        return self.graphql(query, None)['account_statuses']['entities']
    
    
    def getDhcpServers(self):
        query = """{
                    dhcp_servers(paginator:{page:1, records_per_page:1000000}){
                        entities{
                        id
                        name
                        ip_address
                        ip_pools{
                            entities{
                            id
                            name
                            subnet{
                                subnet
                            }
                            ips_available
                            ip_range
                            }
                        }
                        }
                    }
                    }"""
        return self.graphql(query, None)['dhcp_servers']['entities']
    

