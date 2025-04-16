from typing import Optional, Dict, List, Any, Union, Tuple
import pandas as pd
from google.cloud import bigquery, storage
from google.oauth2 import service_account
from google.api_core import exceptions as google_exceptions
import datetime
import pandas_gbq
import os
from google.api_core import exceptions
import pyarrow.parquet as parquet
from pathlib import Path
import json
import dotenv


class BigQueryClient:
    def __init__(
                self, 
                project_id: str, 
                dataset_id: str, 
                key_file: str
                ):
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.key_file = key_file

        self.client = None
        self.credentials = None
        self.job_config = None
        self.full_table_id = None
        self.sql = None
        
        self.default_path = Path('/tmp/data/bigquery/')
        if not self.default_path.exists():
            self.default_path.mkdir(parents=True)

        if self.key_file:
            self.credentials = service_account.Credentials.from_service_account_file(
                self.key_file,
                scopes=["https://www.googleapis.com/auth/cloud-platform"],
            )
            self.client = bigquery.Client(
                credentials=self.credentials,
                project=self.credentials.project_id,
            )

        
        

    def get_client(self):
        return BigQueryClient(
            self.project_id, 
            self.dataset_id, 
            self.key_file
        )

    def show(self) -> None:
        # Use a consistent format for better readability
        config_info = {
            "GCP Configuration": {
                "Project ID": self.project_id,
                "Dataset ID": self.dataset_id,
                "Bucket Name": self.bucket_name or "Not set"
            },
            "Client Status": {
                "BigQuery Client": "Initialized" if self.client else "Not initialized",
                "Credentials": "Set" if self.credentials else "Not set"
            },
            "File Configuration": {
                "Default Path": str(self.default_path),
                "Key File": self.key_file or "Not set",
                "Output Path": str(self.output_path) if self.output_path else "Not set"
            }
        }

        # Print with clear section formatting
        for section, details in config_info.items():
            print(f"\n{section}:")
            print("-" * (len(section) + 1))
            for key, value in details.items():
                print(f"{key:15}: {value}")
    

    def close(self) -> bool:
        """Close the BigQuery client and clean up resources.
        
        This method ensures proper cleanup of the BigQuery client connection
        and associated resources. If no client exists, it will return silently.
        
        The method will attempt to clean up all resources even if an error occurs
        during client closure.
        
        Returns:
            bool: True if cleanup was successful, False if an error occurred
        """
        # Early return if there's no client to close
        if not hasattr(self, 'client') or self.client is None:
            return True
        
        success = True
        
        try:
            self.client.close()
        except Exception as e:
            print(f"Warning: Error while closing client: {str(e)}")
            success = False
        finally:
            # Define all attributes to reset in a list for maintainability
            attrs_to_reset = [
                'client', 'credentials', 'job_config',
                'sql', 'bucket_name', 'default_path', 'output_path'
            ]
            
            # Reset all attributes to None
            for attr in attrs_to_reset:
                if hasattr(self, attr):
                    setattr(self, attr, None)
                    
        return success
    


    def __del__(self):
        """Destructor to ensure proper cleanup of resources."""
        self.close()
    


    def run_sql(self, sql: str) -> None:
        if sql is None:
            raise ValueError("sql must be a non-empty string")
        
        # Check if SQL contains DELETE or TRUNCATE operations
        sql_upper = sql.upper()
        if "DELETE" in sql_upper or "TRUNCATE" in sql_upper:
            print("ERROR: Cannot execute DELETE or TRUNCATE operations for safety reasons")
            return
        
        try:
            self.client.query(sql)
            print("Query run complete")
        except Exception as e:
            print(f"Error running query: {str(e)}")

    def sql2df(self, sql: str = None) -> Optional[pd.DataFrame]:
        if sql is None or not sql.strip():
            raise ValueError("sql must be a non-empty string")
        
        # Check if SQL contains DELETE or TRUNCATE operations
        sql_upper = sql.upper()
        if "DELETE" in sql_upper or "TRUNCATE" in sql_upper:
            print("ERROR: Cannot execute DELETE or TRUNCATE operations for safety reasons")
            return None
        
        try:
            query_job = self.client.query(sql)
            return query_job.to_dataframe()
        except Exception as e:
            print(f"Error running query: {str(e)}")
            return None

    
    def df2table(self, df: pd.DataFrame, 
                 table_id: str, 
                 if_exists: str = 'fail',
                 loading_method: str = 'load_csv',
                 schema: Optional[List[Dict[str, Any]]] = None) -> bool:
        """
        Upload a pandas DataFrame to a BigQuery table using pandas_gbq.
        
        Args:
            df (pd.DataFrame): The DataFrame to upload
            table_id (str): Target table ID
            if_exists (str): Action if table exists: 'fail', 'replace', or 'append'
            schema (Optional[List[Dict[str, Any]]]): BigQuery schema for the table
        
        Returns:
            bool: True if upload was successful, False otherwise
        
        Raises:
            ValueError: If DataFrame is empty or parameters are invalid
        """
        # Input validation
        if df is None or df.empty:
            raise ValueError("DataFrame cannot be None or empty")
        
        if if_exists not in ('fail', 'replace', 'append'):
            raise ValueError("if_exists must be one of: 'fail', 'replace', 'append'")
        
        # Set target table
        target_table_id = table_id
        if not target_table_id:
            raise ValueError("No table_id provided (neither in method call nor in instance)")
        
        # Construct full table ID
        full_table_id = f"{self.dataset_id}.{target_table_id}"
        
        try:
            # Use pandas_gbq to upload the DataFrame
            pandas_gbq.to_gbq(
                df,
                destination_table=full_table_id,
                project_id=self.project_id,
                if_exists=if_exists,
                table_schema=schema,
                credentials=self.credentials,  # Pass the credentials
                api_method=loading_method,
                progress_bar=True  # Enable progress bar
            )
            
            print(f"Successfully uploaded {len(df)} rows to {self.project_id}.{full_table_id}")
            return True
            
        except Exception as e:
            print(f"Error uploading DataFrame to BigQuery: {str(e)}")
            return False

    def sql2gcs(self, sql: str,
                           destination_uri: str,
                           format: str = 'PARQUET',
                           compression: str = 'SNAPPY',
                           create_temp_table: bool = True,
                           wait_for_completion: bool = True,
                           timeout: int = 300,
                           use_sharding: bool = True) -> bool:
        """
        Export BigQuery query results directly to Google Cloud Storage without downloading data locally.
        This uses BigQuery's extract job functionality for efficient data transfer.
        
        Args:
            sql (str): The SQL query to execute
            destination_uri (str): GCS URI to export to (e.g., 'gs://bucket-name/path/to/file')
                                  For large datasets, use a wildcard pattern like 'gs://bucket-name/path/to/file-*.parquet'
                                  or set use_sharding=True to automatically add the wildcard
            format (str): Export format ('PARQUET', 'CSV', 'JSON', 'AVRO')
            compression (str): Compression type ('NONE', 'GZIP', 'SNAPPY', 'DEFLATE')
            create_temp_table (bool): Whether to create a temporary table for the results
            wait_for_completion (bool): Whether to wait for the export job to complete
            timeout (int): Timeout in seconds for waiting for job completion
            use_sharding (bool): Whether to use sharded export with wildcards. If True and destination_uri doesn't
                                contain wildcards, '-*.ext' will be added before the extension.
            
        Returns:
            bool: True if export was successful, False otherwise
        """
        # Input validation
        if sql is None or not sql.strip():
            raise ValueError("SQL query cannot be None or empty")
            
        if not destination_uri or not destination_uri.startswith('gs://'):
            raise ValueError("Destination URI must be a valid GCS path starting with 'gs://'")
            
        # Validate format and compression
        format = format.upper()
        compression = compression.upper()
        
        valid_formats = ['PARQUET', 'CSV', 'JSON', 'AVRO']
        valid_compressions = ['NONE', 'GZIP', 'SNAPPY', 'DEFLATE']
        
        if format not in valid_formats:
            raise ValueError(f"Format must be one of {valid_formats}")
            
        if compression not in valid_compressions:
            raise ValueError(f"Compression must be one of {valid_compressions}")
        
        # Check if sharding is needed and add a wildcard pattern if necessary
        if use_sharding and '*' not in destination_uri:
            # Extract file extension if any
            file_extension = ''
            if '.' in destination_uri.split('/')[-1]:
                base_name, file_extension = os.path.splitext(destination_uri)
                destination_uri = f"{base_name}-*{file_extension}"
            else:
                # No extension, just add the wildcard at the end
                destination_uri = f"{destination_uri}-*"
                
            print(f"Enabled sharding with destination URI: {destination_uri}")
        
        try:
            # BigQuery extract job requires a table as the source, not a query directly
            # So we first need to either run the query to a destination table or use a temporary table
            
            if create_temp_table:
                # Create a temporary table to hold the query results
                temp_table_id = f"temp_export_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
                temp_table_ref = f"{self.project_id}.{self.dataset_id}.{temp_table_id}"
                
                print(f"Creating temporary table {temp_table_ref} for query results...")
                
                # Create a job config for the query
                job_config = bigquery.QueryJobConfig(
                    destination=temp_table_ref,
                    write_disposition="WRITE_TRUNCATE"
                )
                
                # Run the query to the temporary table
                query_job = self.client.query(sql, job_config=job_config)
                query_job.result()  # Wait for query to complete
                
                print(f"Query executed successfully, results stored in temporary table")
                
                # Now set up the source table for the extract job
                source_table = self.client.get_table(temp_table_ref)
            else:
                # When not using a temporary table, we need to create a destination table
                # in a different way as RowIterator doesn't have a .table attribute
                print("Running query and creating temporary destination...")
                
                # Generate a unique job ID
                job_id = f"export_job_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
                
                # Create a destination table with a temporary name
                temp_table_id = f"temp_export_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
                temp_table_ref = f"{self.project_id}.{self.dataset_id}.{temp_table_id}"
                
                # Configure the query job with the destination
                job_config = bigquery.QueryJobConfig(
                    destination=temp_table_ref,
                    write_disposition="WRITE_TRUNCATE"
                )
                
                # Run the query
                query_job = self.client.query(
                    sql,
                    job_config=job_config,
                    job_id=job_id
                )
                
                # Wait for query to complete
                query_job.result()
                
                # Get the destination table reference
                source_table = self.client.get_table(temp_table_ref)
                
                print(f"Query executed successfully, temporary results available")
            
            # Configure the extract job
            extract_job_config = bigquery.ExtractJobConfig()
            extract_job_config.destination_format = format
            
            # Set compression if not NONE
            if compression != 'NONE':
                extract_job_config.compression = compression
                
            # Start the extract job
            print(f"Starting extract job to {destination_uri}")
            extract_job = self.client.extract_table(
                source_table,
                destination_uri,
                job_config=extract_job_config
            )
            
            # Wait for the job to complete if requested
            if wait_for_completion:
                print(f"Waiting for extract job to complete (timeout: {timeout} seconds)...")
                extract_job.result(timeout=timeout)  # Wait for the job to complete
                print(f"Extract job completed successfully")
                
                # Clean up temporary table if created
                if create_temp_table:
                    print(f"Cleaning up temporary table {temp_table_ref}")
                    self.client.delete_table(temp_table_ref)
                
            else:
                print(f"Extract job started (job_id: {extract_job.job_id})")
                print(f"You can check the job status in the BigQuery console")
            
            return True
            
        except Exception as e:
            print(f"Error exporting query results to GCS: {str(e)}")
            return False


    def gcs2table(self, gcs_uri: str, 
                 table_id: str, 
                 schema: Optional[List] = None, 
                 write_disposition: str = 'WRITE_EMPTY', 
                 source_format: str = 'PARQUET',
                 allow_jagged_rows: bool = False,
                 ignore_unknown_values: bool = False,
                 max_bad_records: int = 0) -> bool:
        """
        Loads data from Google Cloud Storage directly into a BigQuery table.
        Uses GCP's native loading capabilities without requiring local resources.
        
        Args:
            gcs_uri: URI of the GCS source file(s) (
                    e.g., 'gs://bucket/folder/file.parquet' 
                    or 'gs://bucket/folder/files-*.csv'
                    or 'gs://bucket/folder/*'
                    )
            table_id: Destination table ID in format 'dataset.table_name' or fully qualified
                     'project.dataset.table_name'
            schema: Optional table schema as a list of SchemaField objects. 
                   If None, schema is auto-detected (except for CSV).
            write_disposition: How to handle existing data in the table, one of:
                              'WRITE_TRUNCATE' (default): Overwrite the table
                              'WRITE_APPEND': Append to the table
                              'WRITE_EMPTY': Only write if table is empty
            source_format: Format of the source data, one of:
                          'PARQUET' (default), 'CSV', 'JSON', 'AVRO', 'ORC'
            allow_jagged_rows: For CSV only. Allow missing trailing optional columns.
            ignore_unknown_values: Ignore values that don't match schema.
            max_bad_records: Max number of bad records allowed before job fails.
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            from google.cloud.bigquery import LoadJobConfig, SourceFormat
            from google.cloud.bigquery.job import WriteDisposition
            
            # Parse write_disposition and source_format
            write_modes = {
                'WRITE_TRUNCATE': WriteDisposition.WRITE_TRUNCATE,
                'WRITE_APPEND': WriteDisposition.WRITE_APPEND,
                'WRITE_EMPTY': WriteDisposition.WRITE_EMPTY,
            }
            
            formats = {
                'PARQUET': SourceFormat.PARQUET,
                'CSV': SourceFormat.CSV,
                'JSON': SourceFormat.NEWLINE_DELIMITED_JSON,
                'AVRO': SourceFormat.AVRO,
                'ORC': SourceFormat.ORC,
            }
            
            # Validate inputs
            if write_disposition not in write_modes:
                raise ValueError(f"write_disposition must be one of: {', '.join(write_modes.keys())}")
            if source_format not in formats:
                raise ValueError(f"source_format must be one of: {', '.join(formats.keys())}")
            
            # Set up job configuration
            job_config = LoadJobConfig()
            job_config.write_disposition = write_modes[write_disposition]
            job_config.source_format = formats[source_format]
            
            # Set schema if provided, otherwise auto-detect (except for CSV)
            if schema is not None:
                job_config.schema = schema
            elif source_format == 'CSV':
                # CSV requires a schema
                job_config.autodetect = True
            else:
                job_config.autodetect = True
            
            # Additional settings
            if source_format == 'CSV':
                job_config.allow_jagged_rows = allow_jagged_rows
                job_config.skip_leading_rows = 1  # Assume header by default
            
            job_config.ignore_unknown_values = ignore_unknown_values
            job_config.max_bad_records = max_bad_records
            
            # Fully qualify the table_id if needed
            if '.' not in table_id:
                # Just table name without dataset, add dataset and project
                table_id = f"{self.project_id}.{self.dataset_id}.{table_id}"
            elif table_id.count('.') == 1:
                # table_id is in format 'dataset.table'
                table_id = f"{self.project_id}.{table_id}"
            
            # Start the load job
            print(f"Loading data from {gcs_uri} into table {table_id} using format {source_format}...")
            if hasattr(self.client, '_credentials'):
                # Reuse the credentials from the BigQuery client
                storage_client = storage.Client(
                    project=self.project_id,
                    credentials=self.client._credentials
                )
            else:
                # Fallback to default credentials if unable to reuse
                storage_client = storage.Client(project=self.project_id)
            
            load_job = self.client.load_table_from_uri(
                gcs_uri,
                table_id,
                job_config=job_config
            )
            
            # Wait for job to complete
            load_job.result()  # This waits for the job to finish and raises an exception if fails
            
            # Get result information
            destination_table = self.client.get_table(table_id)
            print(f"Loaded {destination_table.num_rows} rows into {table_id}")
            return True
            
        except Exception as e:
            print(f"Error loading data from GCS to table: {str(e)}")
            return False

    def delete_gcs_folder(self, gcs_folder_path: str, dry_run: bool = False) -> Tuple[bool, int]:
        """
        Delete a folder and all its contents from Google Cloud Storage.
        
        Args:
            gcs_folder_path: GCS path to the folder to delete 
                            (e.g., 'gs://bucket/folder/' or 'gs://bucket/folder')
            dry_run: If True, only list objects that would be deleted without actually deleting
                   
        Returns:
            Tuple of (success, count) where:
            - success: Boolean indicating if the operation was successful
            - count: Number of objects deleted
        """
        try:
            from google.cloud import storage
            
            # Validate the GCS path
            if not gcs_folder_path.startswith('gs://'):
                raise ValueError("GCS path must start with 'gs://'")
            
            # Normalize the path - ensure it ends with a slash for proper prefix matching
            if not gcs_folder_path.endswith('/'):
                gcs_folder_path += '/'
                
            # Parse the GCS path to get bucket and prefix
            path_without_prefix = gcs_folder_path[5:]  # Remove 'gs://'
            bucket_name = path_without_prefix.split('/')[0]
            folder_prefix = '/'.join(path_without_prefix.split('/')[1:])
            
            # Create a storage client reusing BigQuery credentials if possible
            if hasattr(self.client, '_credentials'):
                storage_client = storage.Client(
                    project=self.project_id,
                    credentials=self.client._credentials
                )
            else:
                storage_client = storage.Client(project=self.project_id)
            
            # Get the bucket
            bucket = storage_client.get_bucket(bucket_name)
            
            # List all blobs with the folder prefix
            blobs = list(bucket.list_blobs(prefix=folder_prefix))
            
            # Count blobs to be deleted
            count = len(blobs)
            
            if count == 0:
                print(f"No objects found in folder: {gcs_folder_path}")
                return True, 0
            
            # If this is a dry run, just print what would be deleted
            if dry_run:
                print(f"DRY RUN: Would delete {count} objects from {gcs_folder_path}:")
                for blob in blobs:
                    print(f" - gs://{bucket_name}/{blob.name}")
                return True, count
            
            # Delete all blobs in parallel
            print(f"Deleting {count} objects from {gcs_folder_path}")
            bucket.delete_blobs(blobs)
                
            print(f"Successfully deleted {count} objects from {gcs_folder_path}")
            return True, count
            
        except Exception as e:
            print(f"Error deleting GCS folder: {str(e)}")
            return False, 0

    def create_gcs_folder(self, gcs_folder_path: str) -> bool:
        """
        Create a folder in Google Cloud Storage.
        
        In GCS, folders are virtual constructs. This method creates a zero-byte object 
        with the folder name that ends with a slash, making it appear as a folder in 
        the GCS console.
        
        Args:
            gcs_folder_path: Path to folder to create, must end with '/'
                            (e.g., 'gs://bucket/folder/')
                            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            from google.cloud import storage
            
            # Validate the GCS path
            if not gcs_folder_path.startswith('gs://'):
                raise ValueError("GCS path must start with 'gs://'")
                
            if not gcs_folder_path.endswith('/'):
                gcs_folder_path += '/'  # Ensure path ends with /
                
            # Parse the GCS path to get bucket and folder path
            path_without_prefix = gcs_folder_path[5:]  # Remove 'gs://'
            bucket_name = path_without_prefix.split('/')[0]
            folder_path = '/'.join(path_without_prefix.split('/')[1:])
            
            # Create a storage client reusing BigQuery credentials if possible
            if hasattr(self.client, '_credentials'):
                storage_client = storage.Client(
                    project=self.project_id, 
                    credentials=self.client._credentials
                )
            else:
                storage_client = storage.Client(project=self.project_id)
                
            # Get the bucket
            bucket = storage_client.get_bucket(bucket_name)
            
            # Create a marker blob with slash at the end (Google's convention)
            marker_blob = bucket.blob(folder_path)
            marker_blob.upload_from_string('', content_type='application/x-directory')
            
            print(f"Successfully created folder: {gcs_folder_path}")
            return True
            
        except Exception as e:
            print(f"Error creating GCS folder: {str(e)}")
            return False
