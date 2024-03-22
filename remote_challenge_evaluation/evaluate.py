import random
from pycocotools.coco import COCO
from evaluation_script.cocoeval_mp import COCOevalMP

def evaluate(test_annotation_file, user_submission_file, phase_codename, **kwargs):
    print("Starting Evaluation.....")
    """
    Evaluates the submission for a particular challenge phase and returns score
    Arguments:

        `test_annotations_file`: Path to test_annotation_file on the server
        `user_submission_file`: Path to file submitted by the user
        `phase_codename`: Phase to which submission is made

        `**kwargs`: keyword arguments that contains additional submission
        metadata that challenge hosts can use to send slack notification.
        You can access the submission metadata
        with kwargs['submission_metadata']

        Example: A sample submission metadata can be accessed like this:
        >>> print(kwargs['submission_metadata'])
        {
            'status': u'running',
            'when_made_public': None,
            'participant_team': 5,
            'input_file': 'https://abc.xyz/path/to/submission/file.json',
            'execution_time': u'123',
            'publication_url': u'ABC',
            'challenge_phase': 1,
            'created_by': u'ABC',
            'stdout_file': 'https://abc.xyz/path/to/stdout/file.json',
            'method_name': u'Test',
            'stderr_file': 'https://abc.xyz/path/to/stderr/file.json',
            'participant_team_name': u'Test Team',
            'project_url': u'http://foo.bar',
            'method_description': u'ABC',
            'is_public': False,
            'submission_result_file': 'https://abc.xyz/path/result/file.json',
            'id': 123,
            'submitted_at': u'2017-03-20T19:22:03.880652Z'
        }
    """
    v3det_gt = COCO(test_annotation_file)  # gt annotation file
    v3det_dt = v3det_gt.loadRes(user_submission_file)  # coco-format det results
    v3det_eval = COCOevalMP(v3det_gt, v3det_dt, 'bbox', num_proc=8)
    v3det_eval.params.maxDets = [300]

    v3det_eval.evaluate()
    v3det_eval.accumulate()
    v3det_eval.summarize()
    # output = {}
    # if phase_codename == "dev":
    #     print("Evaluating for Dev Phase")
    #     output["result"] = [
    #         {
    #             "train_split": {
    #                 "Metric1": random.randint(0, 99),
    #                 "Metric2": random.randint(0, 99),
    #                 "Metric3": random.randint(0, 99),
    #                 "Total": random.randint(0, 99),
    #             }
    #         }
    #     ]
    #     # To display the results in the result file
    #     output["submission_result"] = output["result"][0]["train_split"]
    #     print("Completed evaluation for Dev Phase")
    # elif phase_codename == "test":
    #     print("Evaluating for Test Phase")
    #     output["result"] = [
    #         {
    #             "train_split": {
    #                 "Metric1": random.randint(0, 99),
    #                 "Metric2": random.randint(0, 99),
    #                 "Metric3": random.randint(0, 99),
    #                 "Total": random.randint(0, 99),
    #             }
    #         },
    #         {
    #             "test_split": {
    #                 "Metric1": random.randint(0, 99),
    #                 "Metric2": random.randint(0, 99),
    #                 "Metric3": random.randint(0, 99),
    #                 "Total": random.randint(0, 99),
    #             }
    #         },
    #     ]
    #     # To display the results in the result file
    #     output["submission_result"] = output["result"][0]
    #     print("Completed evaluation for Test Phase")
    # output = dict()
    # output['result'] = "empty"
    # return output

    output = {}
    if phase_codename == "dev":
        print("Evaluating for Dev Phase")
        output["result"] = [
            {
                "OVD": {
                    "bAP": random.randint(0, 99),
                    "nAP": random.randint(0, 99),
                    "AP": random.randint(0, 99),
                }
            }
        ]
        print("Completed evaluation for Dev Phase")
    elif phase_codename == "test":
        print("Evaluating for Test Phase")
        output["result"] = [
            {
                "split": "train_split",
                "show_to_participant": True,
                "accuracies": {"Metric1": 90},
            },
            {
                "split": "test_split",
                "show_to_participant": False,
                "accuracies": {"Metric1": 50, "Metric2": 40},
            },
        ]
        print("Completed evaluation for Test Phase")
    return output
