from airflow_client.client import Configuration, ApiClient
def get_dag():
    """
    This function gets the DAG list, tasks for a DAG, triggers a DAG run, and retrieves the current configuration.
    """
    configuration = airflow_client.client.Configuration(
    host="https://8080-gautami2607-widgetware-1ptoiio9qey.ws-us105.gitpod.io/api/v1",
    username='airflow',
    password='airflow'
    )

# Make sure in the [core] section, the  `load_examples` config is set to True in your airflow.cfg
# or AIRFLOW__CORE__LOAD_EXAMPLES environment variable set to True
    DAG_ID = "forex_data_pipeline"

# Enter a context with an instance of the API client
    with airflow_client.client.ApiClient(configuration) as api_client:

        errors = False

        print('[blue]Getting DAG list')
        dag_api_instance = dag_api.DAGApi(api_client)
        try:
            api_response = dag_api_instance.get_dags()
            print(api_response)
        except airflow_client.client.OpenApiException as e:
            print("[red]Exception when calling DagAPI->get_dags: %s\n" % e)
            errors = True
        else:
            print('[green]Getting DAG list successful')


        print('[blue]Getting Tasks for a DAG')
        try:
            api_response = dag_api_instance.get_tasks(DAG_ID)
            print(api_response)
        except airflow_client.client.exceptions.OpenApiException as e:
            print("[red]Exception when calling DagAPI->get_tasks: %s\n" % e)
            errors = True
        else:
            print('[green]Getting Tasks successful')


        print('[blue]Triggering a DAG run')
        dag_run_api_instance = dag_run_api.DAGRunApi(api_client)
        try:
            # Create a DAGRun object (no dag_id should be specified because it is read-only property of DAGRun)
            # dag_run id is generated randomly to allow multiple executions of the script
            dag_run = DAGRun(
                dag_run_id='some_test_run_' + uuid.uuid4().hex,
            )
            api_response = dag_run_api_instance.post_dag_run(DAG_ID, dag_run)
            print(api_response)
        except airflow_client.client.exceptions.OpenApiException as e:
            print("[red]Exception when calling DAGRunAPI->post_dag_run: %s\n" % e)
            errors = True
        else:
            print('[green]Posting DAG Run successful')

        # Get current configuration. Note, this is disabled by default with most installation.
        # You need to set `expose_config = True` in Airflow configuration in order to retrieve configuration.
        conf_api_instance = config_api.ConfigApi(api_client)
        try:
            api_response = conf_api_instance.get_config()
            print(api_response)
        except airflow_client.client.OpenApiException as e:
            print("[red]Exception when calling ConfigApi->get_config: %s\n" % e)
            errors = True
        else:
            print('[green]Config retrieved successfully')

        if errors:
            print ('\n[red]There were errors while running the script - see above for details')
        else:
            print ('\n[green]Everything went well')