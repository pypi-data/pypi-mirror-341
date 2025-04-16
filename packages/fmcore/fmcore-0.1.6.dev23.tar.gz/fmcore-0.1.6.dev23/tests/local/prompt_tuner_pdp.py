import asyncio

from fmcore.prompt_tuner import BasePromptTuner
from fmcore.prompt_tuner.dspy.optimizer_wrapper import MIPROv2OptimizerConfig
from fmcore.prompt_tuner.types.prompt_tuner_types import PromptTunerConfig

async def prompt_tuner_with_llm_as_judge_boolean():
    product_type: str = "HEADPHONES"
    attribute: str = "earpiece_shape"
    prompt_tuner_config = {
        "task_type": "TEXT_GENERATION",
        "dataset_config": {
                "inputs": {
                    "TRAIN": {
                        "path": f"s3://iml-development-us-east-1/starfish/data/train/{product_type}_{attribute}.parquet",
                        "storage": "S3",
                        "format": "PARQUET",
                    },
                    "TEST": {
                        "path": f"s3://iml-development-us-east-1/starfish/data/test/{product_type}_{attribute}.parquet",
                        "storage": "S3",
                        "format": "PARQUET",
                    },
                },
                "output": {
                    "name": "results",
                    "path": f"s3://iml-development-us-east-1/starfish/output/{product_type}_{attribute}.parquet",
                    "storage": "S3",
                    "format": "PARQUET",
                },
            },
        "prompt_config": {
            "prompt": "ROLE: You are a Catalog Expert. You analyze product information and you are trying your best to infer missing attribute values.\n\nAnalyze the provided Amazon product information in JSON format, detailed above, to determine the value in English of a specific attribute.\n\nYour task is to thoroughly examine the product details. If the attribute's value is clearly inferable from the provided information, make an accurate prediction. \nIn scenarios where the value cannot be deduced, indicate this with '[NO]' for Not Obtainable. \nIf the attribute does not pertain to the product, use '[NA]' for Not Applicable. \nEnsure your prediction is compatible with the attribute's data type, such as predicting 'True' or 'False' for Boolean attributes, or an integer for Integer attributes. Avoid using scientific notation for any prediction.\n        \nFocus your analysis on this specific attribute: \nattribute name: cellphone.water_resistance.",
            "input_fields": [{
                    "name": "asin",
                    "description": "This field represent the unique identifier for a product",
                },
                {
                    "name": "product_type",
                    "description": "This fields represent the type of product",
                },
                {
                    "name": "attribute",
                    "description": "This field represents the attribute to be extracted",
                },
                {
                    "name": "asin_info",
                    "description": "This field represent the information related to product",
                },
                {
                    "name": "attribute_instructions",
                    "description": "This field represent the additional information related to product like possible values for attribute_value",
                },
            ],
            "output_fields": [{
                "name": "attribute_value",
                "description": "This field represent the value extracted for the given attribute_name from the product",
            }],
        },
        "framework": "DSPY",
        "optimizer_config": {
            "optimizer_type": "MIPRO_V2",
            "student_config": {
                'provider_type': 'LAMBDA',
                'model_id': 'mistralai/Mistral-Nemo-Instruct-2407',
                'model_params': {
                    'temperature': 1.0,
                    'max_tokens': 1024,
                    'top_p': 0.9
                },
                'provider_params': {
                    'retries': {
                        'max_retries': 3,
                        'backoff_factor': 1.0,
                        'jitter': 1.0,
                        'retryable_exceptions': ['InvalidSignatureException', 'ThrottlingException',
                            'ModelTimeoutException', 'ServiceUnavailableException',
                            'ModelNotReadyException', 'ServiceQuotaExceededException',
                            'ModelErrorException', 'EndpointConnectionError'
                        ]
                    },
                    'rate_limit': {
                        'max_rate': 10000,
                        'time_period': 60
                    },
                    'region': 'us-west-2',
                    "role_arn": "",
                    'function_arn': 'arn:aws:lambda:us-west-2:136238946932:function:MistralNemo'
                }
            },
            "teacher_config": {
                "provider_type": "BEDROCK",
                "model_id": "anthropic.claude-3-5-sonnet-20240620-v1:0",
                "model_params": {
                    "temperature": 0.5,
                    "max_tokens": 1024
                },
                "provider_params_list": [
                    {
                        "retries": {
                            "max_retries": 50
                        },
                        "rate_limit": {
                            "max_rate": 400
                        },
                        "role_arn": "arn:aws:iam::863518436859:role/ModelFactoryBedrockAccessRole",
                        "region": "us-east-1"
                    },
                    {
                        "retries": {
                            "max_retries": 50
                        },
                        "rate_limit": {
                            "max_rate": 400
                        },
                        "role_arn": "arn:aws:iam::615299746603:role/ModelFactoryBedrockAccessRole",
                        "region": "us-east-1"
                    },
                    {
                        "retries": {
                            "max_retries": 50
                        },
                        "rate_limit": {
                            "max_rate": 400
                        },
                        "role_arn": "arn:aws:iam::615299746603:role/ModelFactoryBedrockAccessRole",
                        "region": "us-west-2"
                    },
                    {
                        "retries": {
                            "max_retries": 50
                        },
                        "rate_limit": {
                            "max_rate": 400
                        },
                        "role_arn": "arn:aws:iam::710271919393:role/ModelFactoryBedrockAccessRole",
                        "region": "us-east-1"
                    },
                    {
                        "retries": {
                            "max_retries": 50
                        },
                        "rate_limit": {
                            "max_rate": 400
                        },
                        "role_arn": "arn:aws:iam::710271919393:role/ModelFactoryBedrockAccessRole",
                        "region": "us-west-2"
                    },
                    {
                        "retries": {
                            "max_retries": 50
                        },
                        "rate_limit": {
                            "max_rate": 400
                        },
                        "role_arn": "arn:aws:iam::872515274170:role/ModelFactoryBedrockAccessRole",
                        "region": "us-east-1"
                    },
                    {
                        "retries": {
                            "max_retries": 50
                        },
                        "rate_limit": {
                            "max_rate": 400
                        },
                        "role_arn": "arn:aws:iam::872515274170:role/ModelFactoryBedrockAccessRole",
                        "region": "us-west-2"
                    }
                ]
            },
            "evaluator_config": {
                "evaluator_type": "LLM_AS_A_JUDGE_BOOLEAN",
                "evaluator_params": {
                    "prompt": 'Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.\n\n### Instruction:\nYou are an auditor for Amazon. Your task is to verify the \'earpiece_shape\' of a product in the Amazon catalog. \nYou will be given the Amazon product data and a test value of \'earpiece_shape\'.\nFirst, you need to deduce the earpiece_shape of the product from the Amazon product data.\nThen, you need to compare the earpiece_shape you deduced from the Amazon product data to the test value of earpiece_shape. \nYou need to predict if the test value of \'earpiece_shape\' is \'Correct\', \'Incorrect\', or \'Unknown\' based on the Amazon product data.\nYou also need to give the reason for your prediction.\n\n\n\n### Rules:\nTo ensure accurate predictions, follow these rules in sequence and think step by step before responding.\n\n1. If you cannot deduce the value of the \'earpiece_shape\' from the given product data, predict \'Unknown\'.\n2. If the test value is aligns with the deduced value, predict \'Correct\'.\n3. If the test value is less informative than the deduced value, predict \'Correct\'.\n4. If the test value is more informative than the deduced value, predict \'Correct\'.\n5. Predict \'Incorrect\' if the test value contradicts the deduced value.\n\n\n### Additional information:\nHere is some additional information about \'earpiece_shape\' to help you make highly accurate classifications.\nEarpiece shape refers to the design and form factor of the part of headphones that fits into or around the outer ear, affecting comfort, fit, and aesthetics.\n\n\n### Amazon product data:\nGiven below is the Amazon product data.\n \n{{input}}\n\n### Test value:\nNow verify the test value of the attribute \'earpiece_shape\': \'{{output.attribute_value}}\'.\n\n\n### Output format:\nRemember to make only one overall prediction. Feel free to ignore irrelevant information and only pay close attention to relevant information in product data.\nPlease output the results in the following JSON format. The JSON should not have anything else except the reason and the prediction.\n{\n    "reason": "evidence for the prediction", \n    "prediction": "Correct/Incorrect/Unknown"\n} \nDo not output anything except the JSON. Always begin your output with {.\n\n\n### Response:',
                    "criteria": "prediction == 'Correct'",
                    "llm_config": {
                        "provider_type": "BEDROCK",
                        "model_id": "anthropic.claude-3-haiku-20240307-v1:0",
                        "model_params": {
                            "temperature": 0.5,
                            "max_tokens": 1024
                        },
                        "provider_params_list": [
                            {
                                "retries": {
                                    "max_retries": 50
                                },
                                "rate_limit": {
                                    "max_rate": 400
                                },
                                "role_arn": "arn:aws:iam::863518436859:role/ModelFactoryBedrockAccessRole",
                                "region": "us-east-1"
                            },
                            {
                                "retries": {
                                    "max_retries": 50
                                },
                                "rate_limit": {
                                    "max_rate": 400
                                },
                                "role_arn": "arn:aws:iam::615299746603:role/ModelFactoryBedrockAccessRole",
                                "region": "us-east-1"
                            },
                            {
                                "retries": {
                                    "max_retries": 50
                                },
                                "rate_limit": {
                                    "max_rate": 400
                                },
                                "role_arn": "arn:aws:iam::615299746603:role/ModelFactoryBedrockAccessRole",
                                "region": "us-west-2"
                            },
                            {
                                "retries": {
                                    "max_retries": 50
                                },
                                "rate_limit": {
                                    "max_rate": 400
                                },
                                "role_arn": "arn:aws:iam::710271919393:role/ModelFactoryBedrockAccessRole",
                                "region": "us-east-1"
                            },
                            {
                                "retries": {
                                    "max_retries": 50
                                },
                                "rate_limit": {
                                    "max_rate": 400
                                },
                                "role_arn": "arn:aws:iam::710271919393:role/ModelFactoryBedrockAccessRole",
                                "region": "us-west-2"
                            },
                            {
                                "retries": {
                                    "max_retries": 50
                                },
                                "rate_limit": {
                                    "max_rate": 400
                                },
                                "role_arn": "arn:aws:iam::872515274170:role/ModelFactoryBedrockAccessRole",
                                "region": "us-east-1"
                            },
                            {
                                "retries": {
                                    "max_retries": 50
                                },
                                "rate_limit": {
                                    "max_rate": 400
                                },
                                "role_arn": "arn:aws:iam::872515274170:role/ModelFactoryBedrockAccessRole",
                                "region": "us-west-2"
                            }
                        ]
                    }
                }
            },
            "optimizer_params": {
                "auto": "light",
                "optimizer_metric": "ACCURACY"
            },
        }
    }

    sm_prompt_tuner_config = {
    'task_type': 'TEXT_GENERATION',
    'dataset_config': {
        'inputs': {
            'TRAIN': {
                'name': None,
                'path': 's3://iml-development-us-east-1/starfish/data/train/HEADPHONES_earpiece_shape.parquet',
                'storage': 'S3',
                'format': 'PARQUET',
                'contents': None,
                'file_glob': None,
                'data_schema': None
            },
            'TEST': {
                'name': None,
                'path': 's3://iml-development-us-east-1/starfish/data/test/HEADPHONES_earpiece_shape.parquet',
                'storage': 'S3',
                'format': 'PARQUET',
                'contents': None,
                'file_glob': None,
                'data_schema': None
            }
        },
        'output': {
            'name': 'results',
            'path': 's3://iml-development-us-east-1/starfish/output/HEADPHONES_earpiece_shape.parquet',
            'storage': 'S3',
            'format': 'PARQUET',
            'contents': None,
            'file_glob': None,
            'data_schema': None
        }
    },
    'prompt_config': {
        'prompt': "ROLE: You are a Catalog Expert. You analyze product information and you are trying your best to infer missing attribute values.\n\nAnalyze the provided Amazon product information in JSON format, detailed above, to determine the value in English of a specific attribute.\n\nYour task is to thoroughly examine the product details. If the attribute's value is clearly inferable from the provided information, make an accurate prediction. \nIn scenarios where the value cannot be deduced, indicate this with '[NO]' for Not Obtainable. \nIf the attribute does not pertain to the product, use '[NA]' for Not Applicable. \nEnsure your prediction is compatible with the attribute's data type, such as predicting 'True' or 'False' for Boolean attributes, or an integer for Integer attributes. Avoid using scientific notation for any prediction.\n        \nFocus your analysis on this specific attribute: \nattribute name: headphones.earpiece_shape",
        'input_fields': [{
            'name': 'asin',
            'description': 'This field represent the unique identifier for a product',
            'field_type': 'string'
        }, {
            'name': 'product_type',
            'description': 'This fields represent the type of product',
            'field_type': 'string'
        }, {
            'name': 'attribute',
            'description': 'This field represents the attribute to be extracted',
            'field_type': 'string'
        }, {
            'name': 'asin_info',
            'description': 'This field represent the information related to product',
            'field_type': 'string'
        }, {
            'name': 'attribute_instructions',
            'description': 'This field represent the additional information related to product like possible values for attribute_value',
            'field_type': 'string'
        }],
        'output_fields': [{
            'name': 'attribute_value',
            'description': 'This field represent the value extracted for the given attribute_name from the product',
            'field_type': 'string'
        }]
    },
    'framework': 'DSPY',
    'optimizer_config': {
        'evaluator_config': {
            'evaluator_type': 'LLM_AS_A_JUDGE_BOOLEAN',
            'evaluator_params': {
                'llm_config': {
                    'provider_type': 'BEDROCK',
                    'model_id': 'anthropic.claude-3-5-sonnet-20240620-v1:0',
                    'model_params': {
                        'temperature': 0.5,
                        'max_tokens': 1024,
                        'top_p': 0.5
                    },
                    'provider_params_list': [{
                        'retries': {
                            'max_retries': 50,
                            'backoff_factor': 1.0,
                            'jitter': 1.0,
                            'retryable_exceptions': ['InvalidSignatureException', 'ThrottlingException', 'ModelTimeoutException', 'ServiceUnavailableException', 'ModelNotReadyException', 'ServiceQuotaExceededException', 'ModelErrorException', 'EndpointConnectionError']
                        },
                        'rate_limit': {
                            'max_rate': 50,
                            'time_period': 60
                        },
                        'role_arn': 'arn:aws:iam::863518436859:role/ModelFactoryBedrockAccessRole',
                        'region': 'us-east-1'
                    }, {
                        'retries': {
                            'max_retries': 50,
                            'backoff_factor': 1.0,
                            'jitter': 1.0,
                            'retryable_exceptions': ['InvalidSignatureException', 'ThrottlingException', 'ModelTimeoutException', 'ServiceUnavailableException', 'ModelNotReadyException', 'ServiceQuotaExceededException', 'ModelErrorException', 'EndpointConnectionError']
                        },
                        'rate_limit': {
                            'max_rate': 50,
                            'time_period': 60
                        },
                        'role_arn': 'arn:aws:iam::615299746603:role/ModelFactoryBedrockAccessRole',
                        'region': 'us-east-1'
                    }, {
                        'retries': {
                            'max_retries': 50,
                            'backoff_factor': 1.0,
                            'jitter': 1.0,
                            'retryable_exceptions': ['InvalidSignatureException', 'ThrottlingException', 'ModelTimeoutException', 'ServiceUnavailableException', 'ModelNotReadyException', 'ServiceQuotaExceededException', 'ModelErrorException', 'EndpointConnectionError']
                        },
                        'rate_limit': {
                            'max_rate': 50,
                            'time_period': 60
                        },
                        'role_arn': 'arn:aws:iam::615299746603:role/ModelFactoryBedrockAccessRole',
                        'region': 'us-west-2'
                    }, {
                        'retries': {
                            'max_retries': 50,
                            'backoff_factor': 1.0,
                            'jitter': 1.0,
                            'retryable_exceptions': ['InvalidSignatureException', 'ThrottlingException', 'ModelTimeoutException', 'ServiceUnavailableException', 'ModelNotReadyException', 'ServiceQuotaExceededException', 'ModelErrorException', 'EndpointConnectionError']
                        },
                        'rate_limit': {
                            'max_rate': 50,
                            'time_period': 60
                        },
                        'role_arn': 'arn:aws:iam::710271919393:role/ModelFactoryBedrockAccessRole',
                        'region': 'us-east-1'
                    }, {
                        'retries': {
                            'max_retries': 50,
                            'backoff_factor': 1.0,
                            'jitter': 1.0,
                            'retryable_exceptions': ['InvalidSignatureException', 'ThrottlingException', 'ModelTimeoutException', 'ServiceUnavailableException', 'ModelNotReadyException', 'ServiceQuotaExceededException', 'ModelErrorException', 'EndpointConnectionError']
                        },
                        'rate_limit': {
                            'max_rate': 50,
                            'time_period': 60
                        },
                        'role_arn': 'arn:aws:iam::710271919393:role/ModelFactoryBedrockAccessRole',
                        'region': 'us-west-2'
                    }, {
                        'retries': {
                            'max_retries': 50,
                            'backoff_factor': 1.0,
                            'jitter': 1.0,
                            'retryable_exceptions': ['InvalidSignatureException', 'ThrottlingException', 'ModelTimeoutException', 'ServiceUnavailableException', 'ModelNotReadyException', 'ServiceQuotaExceededException', 'ModelErrorException', 'EndpointConnectionError']
                        },
                        'rate_limit': {
                            'max_rate': 50,
                            'time_period': 60
                        },
                        'role_arn': 'arn:aws:iam::872515274170:role/ModelFactoryBedrockAccessRole',
                        'region': 'us-east-1'
                    }, {
                        'retries': {
                            'max_retries': 50,
                            'backoff_factor': 1.0,
                            'jitter': 1.0,
                            'retryable_exceptions': ['InvalidSignatureException', 'ThrottlingException', 'ModelTimeoutException', 'ServiceUnavailableException', 'ModelNotReadyException', 'ServiceQuotaExceededException', 'ModelErrorException', 'EndpointConnectionError']
                        },
                        'rate_limit': {
                            'max_rate': 50,
                            'time_period': 60
                        },
                        'role_arn': 'arn:aws:iam::872515274170:role/ModelFactoryBedrockAccessRole',
                        'region': 'us-west-2'
                    }]
                },
                'prompt': 'Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.\n\n### Instruction:\nYou are an auditor for Amazon. Your task is to verify the \'earpiece_shape\' of a product in the Amazon catalog. \nYou will be given the Amazon product data and a test value of \'earpiece_shape\'.\nFirst, you need to deduce the earpiece_shape of the product from the Amazon product data.\nThen, you need to compare the earpiece_shape you deduced from the Amazon product data to the test value of earpiece_shape. \nYou need to predict if the test value of \'earpiece_shape\' is \'Correct\', \'Incorrect\', or \'Unknown\' based on the Amazon product data.\nYou also need to give the reason for your prediction.\n\n\n\n\n\n\n### Rules:\nTo ensure accurate predictions, follow these rules in sequence and think step by step before responding.\n\n1. If you cannot deduce the value of the \'earpiece_shape\' from the given product data, predict \'Unknown\'.\n2. If the test value is aligns with the deduced value, predict \'Correct\'.\n3. If the test value is less informative than the deduced value, predict \'Correct\'.\n4. If the test value is more informative than the deduced value, predict \'Correct\'.\n5. Predict \'Incorrect\' if the test value contradicts the deduced value.\n\n\n### Additional information:\nHere is some additional information about \'earpiece_shape\' to help you make highly accurate classifications.\nEarpiece shape refers to the design and form factor of the part of headphones that fits into or around the outer ear, affecting comfort, fit, and aesthetics.\n\n\n### Amazon product data:\nGiven below is the Amazon product data.\n \n{{input}}\n\n### Test value:\nNow verify the test value of the attribute \'earpiece_shape\': \'{{output.attribute_value}}\'.\n\n\n### Output format:\nRemember to make only one overall prediction. Feel free to ignore irrelevant information and only pay close attention to relevant information in product data.\nPlease output the results in the following JSON format. The JSON should not have anything else except the reason and the prediction.\n{\n    "reason": "evidence for the prediction", \n    "prediction": "Correct/Incorrect/Unknown"\n} \nDo not output anything except the JSON. Always begin your output with {.\n\n\n### Response:',
                'criteria': "prediction == 'Correct'"
            }
        },
        'teacher_config': {
            'provider_type': 'BEDROCK',
            'model_id': 'anthropic.claude-3-5-sonnet-20240620-v1:0',
            'model_params': {
                'temperature': 0.5,
                'max_tokens': 1024,
                'top_p': 0.5
            },
            'provider_params_list': [{
                'retries': {
                    'max_retries': 50,
                    'backoff_factor': 1.0,
                    'jitter': 1.0,
                    'retryable_exceptions': ['InvalidSignatureException', 'ThrottlingException', 'ModelTimeoutException', 'ServiceUnavailableException', 'ModelNotReadyException', 'ServiceQuotaExceededException', 'ModelErrorException', 'EndpointConnectionError']
                },
                'rate_limit': {
                    'max_rate': 50,
                    'time_period': 60
                },
                'role_arn': 'arn:aws:iam::863518436859:role/ModelFactoryBedrockAccessRole',
                'region': 'us-east-1'
            }, {
                'retries': {
                    'max_retries': 50,
                    'backoff_factor': 1.0,
                    'jitter': 1.0,
                    'retryable_exceptions': ['InvalidSignatureException', 'ThrottlingException', 'ModelTimeoutException', 'ServiceUnavailableException', 'ModelNotReadyException', 'ServiceQuotaExceededException', 'ModelErrorException', 'EndpointConnectionError']
                },
                'rate_limit': {
                    'max_rate': 50,
                    'time_period': 60
                },
                'role_arn': 'arn:aws:iam::615299746603:role/ModelFactoryBedrockAccessRole',
                'region': 'us-east-1'
            }, {
                'retries': {
                    'max_retries': 50,
                    'backoff_factor': 1.0,
                    'jitter': 1.0,
                    'retryable_exceptions': ['InvalidSignatureException', 'ThrottlingException', 'ModelTimeoutException', 'ServiceUnavailableException', 'ModelNotReadyException', 'ServiceQuotaExceededException', 'ModelErrorException', 'EndpointConnectionError']
                },
                'rate_limit': {
                    'max_rate': 50,
                    'time_period': 60
                },
                'role_arn': 'arn:aws:iam::615299746603:role/ModelFactoryBedrockAccessRole',
                'region': 'us-west-2'
            }, {
                'retries': {
                    'max_retries': 50,
                    'backoff_factor': 1.0,
                    'jitter': 1.0,
                    'retryable_exceptions': ['InvalidSignatureException', 'ThrottlingException', 'ModelTimeoutException', 'ServiceUnavailableException', 'ModelNotReadyException', 'ServiceQuotaExceededException', 'ModelErrorException', 'EndpointConnectionError']
                },
                'rate_limit': {
                    'max_rate': 50,
                    'time_period': 60
                },
                'role_arn': 'arn:aws:iam::710271919393:role/ModelFactoryBedrockAccessRole',
                'region': 'us-east-1'
            }, {
                'retries': {
                    'max_retries': 50,
                    'backoff_factor': 1.0,
                    'jitter': 1.0,
                    'retryable_exceptions': ['InvalidSignatureException', 'ThrottlingException', 'ModelTimeoutException', 'ServiceUnavailableException', 'ModelNotReadyException', 'ServiceQuotaExceededException', 'ModelErrorException', 'EndpointConnectionError']
                },
                'rate_limit': {
                    'max_rate': 50,
                    'time_period': 60
                },
                'role_arn': 'arn:aws:iam::710271919393:role/ModelFactoryBedrockAccessRole',
                'region': 'us-west-2'
            }, {
                'retries': {
                    'max_retries': 50,
                    'backoff_factor': 1.0,
                    'jitter': 1.0,
                    'retryable_exceptions': ['InvalidSignatureException', 'ThrottlingException', 'ModelTimeoutException', 'ServiceUnavailableException', 'ModelNotReadyException', 'ServiceQuotaExceededException', 'ModelErrorException', 'EndpointConnectionError']
                },
                'rate_limit': {
                    'max_rate': 50,
                    'time_period': 60
                },
                'role_arn': 'arn:aws:iam::872515274170:role/ModelFactoryBedrockAccessRole',
                'region': 'us-east-1'
            }, {
                'retries': {
                    'max_retries': 50,
                    'backoff_factor': 1.0,
                    'jitter': 1.0,
                    'retryable_exceptions': ['InvalidSignatureException', 'ThrottlingException', 'ModelTimeoutException', 'ServiceUnavailableException', 'ModelNotReadyException', 'ServiceQuotaExceededException', 'ModelErrorException', 'EndpointConnectionError']
                },
                'rate_limit': {
                    'max_rate': 50,
                    'time_period': 60
                },
                'role_arn': 'arn:aws:iam::872515274170:role/ModelFactoryBedrockAccessRole',
                'region': 'us-west-2'
            }]
        },
        'student_config': {
            'provider_type': 'LAMBDA',
            'model_id': 'mistralai/Mistral-Nemo-Instruct-2407',
            'model_params': {
                'temperature': 1.0,
                'max_tokens': 1024,
                'top_p': 0.9
            },
            'provider_params': {
                'retries': {
                    'max_retries': 3,
                    'backoff_factor': 1.0,
                    'jitter': 1.0,
                    'retryable_exceptions': ['InvalidSignatureException', 'ThrottlingException', 'ModelTimeoutException', 'ServiceUnavailableException', 'ModelNotReadyException', 'ServiceQuotaExceededException', 'ModelErrorException', 'EndpointConnectionError']
                },
                'rate_limit': {
                    'max_rate': 10000,
                    'time_period': 60
                },
                'role_arn': 'arn:aws:iam::136238946932:role/ModelFactoryBedrockAccessRole',
                'region': 'us-west-2',
                'function_arn': 'arn:aws:lambda:us-west-2:136238946932:function:MistralNemo'
            }
        },
        'optimizer_type': 'MIPRO_V2',
        'optimizer_params': {
            'optimizer_metric': 'ACCURACY',
            'num_candidates': 10,
            'minibatch': False
        }
    }
}

    prompt_tuner_config = PromptTunerConfig(**sm_prompt_tuner_config)
    print(prompt_tuner_config.model_dump())
    tuner = BasePromptTuner.of(config=prompt_tuner_config)
    await tuner.tune()



async def main():
    print("Running Prompt Tuner with Classification")
    #await prompt_tuner_with_classification()

    print("Running Prompt Tuner with Boolean as judge")
    await prompt_tuner_with_llm_as_judge_boolean()


if __name__ == "__main__":
    asyncio.run(main())
