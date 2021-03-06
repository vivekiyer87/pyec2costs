#!/usr/bin/env python
import json
import urllib2
import pprint
import logging

ONDEMAND_COSTS_URL = "http://aws.amazon.com/ec2/pricing/pricing-on-demand-instances.json"

EC2_REGION_MAP = {"apac-sin": "ap-northeast-1",
                  "us-west": "us-west-1",
                  "eu-ireland": "eu-west-1",
                  "apac-tokyo": "ap-southeast-1",
                  "apac-syd": "ap-southeast-2",
                  "us-east": "us-east-1",
                  "us-west-2": "us-west-2",
                  "sa-east-1": "sa-east-1"}


def get_current_ondemand_costs():
    """
    Return a dictionary of the current AWS ondemand prices.
    The dictionary is keyed by region. dict[region][instance][os]

    @return: dict,
    """
    prices = {}
    data = json.loads(urllib2.urlopen(ONDEMAND_COSTS_URL).read())

    for region in data["config"]["regions"]:
        region = dict(region)
        try:
            region_string = EC2_REGION_MAP[region["region"]]
            prices[region_string] = {}
            for instance in region["instanceTypes"]:
                inst_type = instance["type"]
                for size in instance["sizes"]:
                    linux_cost = win_cost = 'NA'
                    for values in size["valueColumns"]:
                        if values["name"] == "linux":
                            linux_cost = float(values["prices"]["USD"])
                        elif values["name"] == "mswin":
                            win_cost = float(values["prices"]["USD"])
                    prices[region_string][size["size"]] = {"windows": win_cost, "linux": linux_cost}
        except:
            logging.error("WARNING: Amazon added a new region or instance type that we don't know about yet.")

    return prices


if __name__ == "__main__":
    pprint.pprint(get_current_ondemand_costs())
