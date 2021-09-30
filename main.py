# -*- coding: utf-8 -*-

import json
import os
import sys
import requests
import time
from dotenv import load_dotenv


class Salmonia:
    def __init__(self):
        # ディレクトリの作成
        try:
            os.makedirs("summary")
            os.makedirs("results")
        except:
            pass
        self.iksm_session = os.environ.get("IKSM_SESSION")
        self.api_token = os.environ.get("API_TOKEN")
        self.last_job_id = os.environ.get("LATEST_JOB_NUM")
        self.development = os.environ.get("DEVELOPMENT") == None

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

        self.last_job_id = int(self.last_job_id)

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
                if self.development:
                    with open(f"results/{job_num}.json", mode="w") as f:
                        # JSONを保存
                        json.dump(response.json(), f)
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
            break

    def getLatestJobId(self):
        url = "https://app.splatoon2.nintendo.net/api/coop_results"
        response = requests.get(url, cookies=dict(
            iksm_session=self.iksm_session)).json()
        latest_job_id = response["summary"]["card"]["job_num"]
        if self.development:
            with open("summary/card.json", mode="w") as f:
                # JSONを保存
                json.dump(response["summary"]["card"], f)
        # 新規リザルトがない
        if latest_job_id == self.last_job_id:
            print("No new results")
            sys.exit()
        else:
            return range(max(self.last_job_id + 1, latest_job_id - 49), latest_job_id + 1)


if __name__ == "__main__":
    load_dotenv()
    salmonia = Salmonia()
    salmonia.getResultsFromSplatNet2()
