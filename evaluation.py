import json
import pandas
import numpy


date = "20230710-"
directory = f"./data/{date}/"

evaluation = {}

evaluation["ssa"] = {"run_times": [],
                      "final_value": []}

f = open(f"{directory}/exp_params.json")
parâmetros_da_experimentação = json.load(f)

for i in range(parâmetros_da_experimentação["número_de_execuções"]):

    f = open(f"{directory}/run-SSA-{i}.json")
    j = json.load(f)
    evaluation["ssa"]["run_times"].append(j["execution_time"])
    evaluation["ssa"]["final_value"].append(j["value"][-1])

print("SSA")
print(pandas.DataFrame(evaluation["ssa"]))
print("mean_run_time:", numpy.mean(evaluation["ssa"]["run_times"]))
print("mean_value:", numpy.mean(evaluation["ssa"]["final_value"]))
print()

threads_number = parâmetros_da_experimentação["threads_number"]
k = 0
for k in range(len(threads_number)):

    evaluation[f"psa{threads_number[k]}"] = {"run_times": [],
                                              "final_value": []}

    for i in range(parâmetros_da_experimentação["número_de_execuções"]):

        f = open(f"{directory}/run-PSA{threads_number[k]}-{i}.json")
        j = json.load(f)
        evaluation[f"psa{threads_number[k]}"]["run_times"].append(j["execution_time"])
        evaluation[f"psa{threads_number[k]}"]["final_value"].append(j["value"][-1])

    print(f"PSA-{threads_number[k]}")
    print(pandas.DataFrame(evaluation[f"psa{threads_number[k]}"]))
    print("mean_run_time:", numpy.mean(evaluation[f"psa{threads_number[k]}"]["run_times"]))
    print("mean_value:", numpy.mean(evaluation[f"psa{threads_number[k]}"]["final_value"]))
    print()
