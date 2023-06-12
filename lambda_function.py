import json
from submission_manager import PlatoFormSubmission, DisChargeSubmissionManager


def lambda_handler(event, context):
    body = json.loads(event.get('body'))
    print(event)
    discharge_manager = DisChargeSubmissionManager(PlatoFormSubmission)
    if discharge_manager.process_submission(body, '/tmp/'):
        print('Completed')
        return {
            'statusCode': 201,
            'body': json.dumps('Submission processed successfully')
        }
    else:
         return {
            'statusCode': 500,
            'body': json.dumps('Internal Server Error')
        }

