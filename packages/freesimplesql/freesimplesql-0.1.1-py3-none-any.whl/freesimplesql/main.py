import FreeSimpleGUI as sg
from sqlalchemy.sql import text

from sqlmodel import Field, Session, SQLModel, create_engine, select
from datetime import datetime, timedelta
import random
import ipaddress
import json
from typing import Optional
from faker import Faker
from loguru import logger
from pydantic import field_validator
import shutil

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sn: int
    timestamp: datetime
    src_ip: str
    dst_ip: str
    msg_name: str
    msg_content: str
    hexvalue: str

    @field_validator("timestamp", mode="before")
    def validate_timestamp(cls, value):
        if isinstance(value, str):
            return datetime.fromisoformat(value)
        return value

class DBBrowser:
    def __init__(self):
        self.engine = create_engine("sqlite:///database.db", echo=False)
        self.page_size = 50 * 10
        self.default_query = "SELECT * FROM message"
        self.current_page = 0
        self.total_rows = 0

    @staticmethod
    def setup_db():
        SQLModel.metadata.create_all(DBBrowser.create_engine())
        with Session(DBrowser.create_engine()) as session:
            if not session.exec(select(Message)).first():
                DBrowser.generate_dummy_data()

    @staticmethod
    def create_engine():
        return create_engine("sqlite:///database.db", echo=False)

    @staticmethod
    def generate_dummy_data():
        fake = Faker()
        msg_names = ["INFO", "WARNING", "ERROR", "DEBUG", "CRITICAL"]
        base_time = datetime.now()
        with Session(DBrowser.create_engine()) as session:
            messages = []
            for i in range(1000):
                json_content = {
                    "id": i + 1,
                    "name": fake.name(),
                    "email": fake.email(),
                    "address": fake.address(),
                    "text": fake.text(max_nb_chars=900)
                }
                json_str = json.dumps(json_content)
                hex_value = json_str.encode("utf-8").hex()
                message = Message(
                    sn=i + 1,
                    timestamp=base_time + timedelta(seconds=i),
                    src_ip=str(ipaddress.IPv4Address(random.randint(0, 2**32-1))),
                    dst_ip=str(ipaddress.IPv4Address(random.randint(0, 2**32-1))),
                    msg_name=random.choice(msg_names),
                    msg_content=json_str,
                    hexvalue=hex_value
                )
                messages.append(message)
            session.add_all(messages)
            session.commit()

    def execute_query(self, query_text=None):
        with Session(self.engine) as session:
            try:
                # Calculate LIMIT and OFFSET for pagination
                limit = self.page_size
                offset = self.current_page * self.page_size
                paginated_query = None
                if query_text and query_text.strip():
                    # Remove any existing LIMIT/OFFSET from user query for safety
                    base_query = query_text.strip().rstrip(';')
                    if 'limit' in base_query.lower():
                        base_query = base_query.rsplit('limit', 1)[0].strip()
                    paginated_query = f"{base_query} LIMIT {limit} OFFSET {offset}"
                    logger.debug(f"Executing paginated SQL query: {paginated_query}")
                    result = session.exec(text(paginated_query))
                    all_results = [Message(**dict(zip(result.keys(), row))) for row in result]
                    # Get total rows for pagination info
                    count_query = f"SELECT COUNT(*) FROM ({base_query}) as subquery"
                    total = session.exec(text(count_query)).first()
                    self.total_rows = total[0] if total else 0
                else:
                    logger.debug("Executing default paginated query using SQLModel")
                    result = session.exec(select(Message).offset(offset).limit(limit))
                    all_results = list(result)
                    # Get total rows for pagination info
                    self.total_rows = session.exec(select(Message)).count()
                logger.debug(f"Query returned {len(all_results)} rows (page {self.current_page + 1})")
                return all_results
            except Exception as e:
                logger.debug(f"Query error: {e}")
                self.total_rows = 0
                return []

    def get_columns(self):
        return ["sn", "timestamp", "src_ip", "dst_ip", "msg_name", "msg_content", "hexvalue"]

    def get_row_dict(self, row: Message):
        return {
            "sn": row.sn,
            "timestamp": row.timestamp,
            "src_ip": row.src_ip,
            "dst_ip": row.dst_ip,
            "msg_name": row.msg_name,
            "msg_content": row.msg_content,
            "hexvalue": row.hexvalue
        }



def main():
    sg.theme('DarkBlue3')
    browser = DBBrowser()
    columns = browser.get_columns()

    current_page_rows = []  # Store the current page's row objects

    def update_table(query_text=None):
        nonlocal current_page_rows
        logger.debug("Updating table with new query results")
        rows = browser.execute_query(query_text)
        table_data = [[getattr(row, col) for col in columns] for row in rows]
        window['-TABLE-'].update(values=table_data)
        current_page_rows = rows  # Store the current page's row objects for later use
        max_pages = (browser.total_rows - 1) // browser.page_size + 1 if browser.total_rows > 0 else 1
        window['-PAGE_INFO-'].update(f"Page {browser.current_page + 1} of {max_pages}")
        logger.debug(f"Table updated. Current page: {browser.current_page + 1}, Total pages: {max_pages}")

    # --- Layout columns ---
    builder_col = sg.Column([
        [sg.Text("SQL Query:")],
        [sg.Multiline(default_text=browser.default_query, size=(60, 5), key='-QUERY-', expand_x=True, expand_y=True)],
        [
            sg.Combo(columns, default_value=columns[0], key='-FILTER-COL-', size=(15, 1)),
            sg.Combo(['=', '!=', '>', '<', 'LIKE'], default_value='=', key='-FILTER-OP-', size=(10, 1)),
            sg.InputText(key='-FILTER-VALUE-', size=(15, 1)),
            sg.Button('ADD', key='-ADD-FILTER-'),
            sg.Button('OR', key='-OR-FILTER-'),
            sg.Button('NOT', key='-NOT-FILTER-'),
            sg.Button(' ( ', key='-OPEN-BRACKET-'),
            sg.Button(' ) ', key='-CLOSE-BRACKET-'),
            sg.Push(),
            sg.Button('Search', key='-SEARCH-'),
            sg.Button('Reset', key='-RESET-'),
            sg.Text('|'),
            sg.Button('Export DB', key='-EXPORT-'),
            sg.Button('Import DB', key='-IMPORT-')
        ],
    ], expand_x=True, expand_y=False)

    history_col = sg.Column([
        [sg.Text("Query History:")],
        [sg.Multiline(size=(30, 7), key='-HISTORY-', disabled=True, expand_x=True, expand_y=True)]
    ], expand_x=True, expand_y=False)

    table_col = sg.Column([
        [sg.Text("Data Table:")],
        [sg.Table(
            values=[],
            headings=columns,
            auto_size_columns=True,
            display_row_numbers=False,
            justification='left',
            num_rows=20,
            key='-TABLE-',
            enable_events=True,
            expand_x=True,
            expand_y=True
        )],
        [
            sg.Button('First', key='-FIRST-'),
            sg.Button('Previous', key='-PREVIOUS-'),
            sg.Text('', key='-PAGE_INFO-', size=(20, 1), justification='center'),
            sg.Button('Next', key='-NEXT-'),
            sg.Button('Last', key='-LAST-')
        ]
    ], expand_x=True, expand_y=True)

    detail_tabs_col = sg.Column([
        [sg.TabGroup([
            [
                sg.Tab('Detail View (JSON)', [[sg.Multiline(size=(50, 30), key='-DETAIL-', disabled=True, expand_x=True, expand_y=True)]], key='-DETAIL-TAB-'),
                sg.Tab('Compact View', [[sg.Multiline(size=(40, 30), key='-COMPACT-', disabled=True, expand_x=True, expand_y=True)]], key='-COMPACT-TAB-')
            ]
        ], key='-TABS-', expand_x=True, expand_y=True)]
    ], expand_x=True, expand_y=True)

    layout = [
        [
            builder_col,
            history_col
        ],
        [
            table_col,
            detail_tabs_col
        ]
    ]

    window = sg.Window('Database Browser', layout, resizable=True, finalize=True, size=(1800, 900))
    # Use LIMIT for the default query
    update_table(browser.default_query)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == '-EXPORT-':
            export_path = sg.popup_get_file('Save database as...', save_as=True, default_extension='.db', file_types=(('SQLite DB', '*.db'),))
            if export_path:
                
                try:
                    shutil.copy('database.db', export_path)
                    logger.debug(f"Database exported to {export_path}")
                    sg.popup('Database exported successfully!', title='Export')
                except Exception as e:
                    sg.popup(f'Export failed: {e}', title='Export Error')
                    logger.debug(f"Export failed: {e}")
                    
        elif event == '-IMPORT-':
            import_path = sg.popup_get_file(
                'Select SQLite database to import',
                file_types=(('SQLite DB', '*.db;*.sqlite;*.sqlite3'),)
            )
            if import_path:
                try:
                    logger.debug(f"Importing database from {import_path}")
                    sg.popup('Database imported successfully! Restarting view...', title='Import')

                    browser.engine = create_engine(f'sqlite:///{import_path}', echo=False)
                    browser.current_page = 0
                    update_table(browser.default_query)
                except Exception as e:
                    sg.popup(f'Import failed: {e}', title='Import Error')
        elif event == '-RESET-':
            browser.current_page = 0
            window['-QUERY-'].update(browser.default_query)  # Reset textarea to default query
            update_table(browser.default_query)
        elif event == '-SEARCH-':
            browser.current_page = 0
            query = values['-QUERY-'].strip()
            if query:
                # Add query to the top of the history
                history = window['-HISTORY-'].get()
                updated_history = f"{query}\n{history}" if history else query
                window['-HISTORY-'].update(updated_history)
                update_table(query)
        elif event == '-NOT-FILTER-':
            col = values['-FILTER-COL-']
            op = values['-FILTER-OP-']
            val = values['-FILTER-VALUE-']
            if col and op and val:
                condition = f"{col} {op} '{val}'"
                current_query = values['-QUERY-'].strip()
                if 'WHERE' in current_query.upper():
                    updated_query = f"{current_query} NOT {condition}"
                else:
                    updated_query = f"{current_query} WHERE {condition}"
                window['-QUERY-'].update(updated_query)                
        elif event == '-ADD-FILTER-':
            col = values['-FILTER-COL-']
            op = values['-FILTER-OP-']
            val = values['-FILTER-VALUE-']
            if col and op and val:
                condition = f"{col} {op} '{val}'"
                current_query = values['-QUERY-'].strip()
                if 'WHERE' in current_query.upper():
                    updated_query = f"{current_query} AND {condition}"
                else:
                    updated_query = f"{current_query} WHERE {condition}"
                window['-QUERY-'].update(updated_query)
        elif event == '-OR-FILTER-':
            col = values['-FILTER-COL-']
            op = values['-FILTER-OP-']
            val = values['-FILTER-VALUE-']
            if col and op and val:
                condition = f"{col} {op} '{val}'"
                current_query = values['-QUERY-'].strip()
                if 'WHERE' in current_query.upper():
                    updated_query = f"{current_query} OR {condition}"
                else:
                    updated_query = f"{current_query} WHERE {condition}"
                window['-QUERY-'].update(updated_query)
        elif event == '-OPEN-BRACKET-':
            current_query = values['-QUERY-'].strip()
            updated_query = f"{current_query} ("
            window['-QUERY-'].update(updated_query)
        elif event == '-CLOSE-BRACKET-':
            current_query = values['-QUERY-'].strip()
            updated_query = f"{current_query} )"
            window['-QUERY-'].update(updated_query)
        elif event == '-FIRST-':
            browser.current_page = 0
            update_table(values['-QUERY-'].strip())
        elif event == '-PREVIOUS-':
            if browser.current_page > 0:
                browser.current_page -= 1
                update_table(values['-QUERY-'].strip())
        elif event == '-NEXT-':
            if (browser.current_page + 1) * browser.page_size < browser.total_rows:
                browser.current_page += 1
                update_table(values['-QUERY-'].strip())
        elif event == '-LAST-':
            browser.current_page = (browser.total_rows - 1) // browser.page_size
            update_table(values['-QUERY-'].strip())
        elif event == '-TABLE-':
            if values['-TABLE-']:
                selected_idx = values['-TABLE-'][0]
                # Use the cached rows for the current page
                rows = current_page_rows
                if selected_idx < len(rows):
                    row = rows[selected_idx]
                    row_dict = browser.get_row_dict(row)
                    if 'msg_content' in row_dict:
                        try:
                            parsed_content = json.loads(row_dict['msg_content'])
                            row_dict['msg_content'] = parsed_content
                        except json.JSONDecodeError:
                            logger.debug("Failed to parse `msg_content` as JSON.")
                    pretty_json = json.dumps(row_dict, indent=4, default=str)
                    window['-DETAIL-'].update(pretty_json)
                    window['-COMPACT-'].update("\n".join([f"{k}: {v}" for k, v in row_dict.items()]))
                else:
                    logger.debug("Selected index is out of range for the query result.")

    window.close()

if __name__ == "__main__":
    main()

