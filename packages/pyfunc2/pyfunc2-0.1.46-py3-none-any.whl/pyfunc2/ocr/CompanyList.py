class CompanyList:
    company_list_array = ["languagetooler", "adobe", "zoom", "ionos", "xolo", "netcup", "strato", "premium", "namesilo", "whmcs",
                          "aftermarket", "Michau", "DigitalOcean", "PERSKIMEDIA", "ICDSoft",
                          "restream", "sav", "github", "zoom", "openai", "zoho", "tuneup", "TuneUp Accounting",
                          "Envato", "dynadot", "wise", "transferwise",
                          "LeapSwitch", "easeus", "sixt", "b.center", "useme", "Universal",
                          # "onlineaccounting",
                          "Top Connect", "bahn", "TRUSTSECURE", "netisar", "linkedin", "holvi", "modulesgarden",
                          "WebSouls",
                          "cloudflare", "namecheap", "ovh", "mserwis", "domeny.tv", "amazon", "microsoft", "porkbun",
                          "zone",
                          "azure", "dd", "aws", "8x8", "88"]

    def __init__(self, company_list_array=[]):
        if company_list_array:
            self.company_list_array = company_list_array

    def sorted_from_shortest_to_longest_name(self):
        # all lower case
        company_list_sorted = [k.lower() for k in self.company_list_array]
        # sort from the longest string to lowest
        company_list_sorted = sorted(company_list_sorted, key=len, reverse=True)

        return company_list_sorted
