# SQLAlchemy History

SQLAlchemy History is an extension for SQLAlchemy that provides change tracking and history logging for SQLAlchemy models. It allows developers to easily track changes to their database objects over time, providing a comprehensive history of modifications.

## Features

- Track changes made to SQLAlchemy models.
- Log historical data for audit purposes.
- Easily integrate with existing SQLAlchemy applications.

## How it works

When you change model fields and add the model to a session, via `session.add(model)` or `session.add_all([model])`, the event listener `"after_update"` you defined is triggered.

This listener monitors for changes to field values. If changes have been made, an object containing the field changes (`HistoryChanges`) will be added to the corresponding table.
