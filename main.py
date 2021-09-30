# -*- coding: utf-8 -*-

import json
import os
import sys
import requests
import time


class Salmonia:
    def __init__(self):
        self.iksm_session = os.environ.get("IKSM_SESSION")
        self.api_token = os.environ.get("API_TOKEN")
        self.last_job_id = int(os.environ.get("LATEST_JOB_NUM"))

        # 環境変数がセットされていない
        if self.iksm_session == None:
            print("NO IKSM_SESSION IS SET")
            sys.exit()
        if self.api_token == None:
            print("NO API_TOKEN IS SET")
            sys.exit()
        if self.last_job_id == None:
            print("NO JOB_ID IS SET")
            sys.exit()

    def getResultsFromSplatNet2(self):
        for job_num in self.getLatestJobId():
            print(f"Getting {job_num} result from SplatNet2")
            url = f"https://app.splatoon2.nintendo.net/api/coop_results/{job_num}"
            response = requests.get(url, cookies=dict(
                iksm_session=self.iksm_session))
            if response.status_code == 403:
                print("Forbidden")
                sys.exit()
            if response.status_code == 404:
                print("Not found")
                continue
            if response.status_code == 200:
                url = "https://salmon-stats-api.yuki.games/api/results"
                header = {"Content-type": "application/json",
                          "Authorization": "Bearer " + self.api_token}
                response = requests.post(url, data=json.dumps(
                    {"results": [response.json()]}), headers=header)
                if response.status_code == 400:
                    print("Bad request")
                    sys.exit()
                if response.status_code == 401:
                    print("Unauthorized")
                    sys.exit()
                if response.status_code == 403:
                    print("Forbidden")
                    sys.exit()
                if response.status_code == 200:
                    print(f"Uploaded {job_num} result to Salmon Stats")
                    # バイトIDをアップデート
                    os.environ["LATEST_JOB_NUM"] = str(job_num)
                time.sleep(5)

    def getLatestJobId(self):
        url = "https://app.splatoon2.nintendo.net/api/coop_results"
        response = requests.get(url, cookies=dict(
            iksm_session=self.iksm_session)).json()
        latest_job_id = response["summary"]["card"]["job_num"]
        # 新規リザルトがない
        if latest_job_id == self.last_job_id:
            print("No new results")
            sys.exit()
        else:
            return range(max(self.last_job_id + 1, latest_job_id - 49), latest_job_id + 1)


if __name__ == "__main__":
    salmonia = Salmonia()

    salmonia.getResultsFromSplatNet2()
