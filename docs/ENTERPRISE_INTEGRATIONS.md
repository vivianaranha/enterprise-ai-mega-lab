# Replacing Mock Systems With Enterprise Integrations

The built-in SQLite database is deliberately hidden behind `EnterpriseTools`. This creates a clean migration path.

## Salesforce

Replace account, contact, opportunity, and activity methods with Salesforce REST API or an MCP/OpenAPI connector.

## ServiceNow

Replace ticket methods with incident, problem, change, and knowledge APIs.

## Workday

Replace employee/workforce methods with approved worker and organization APIs. Keep sensitive HR fields tightly scoped.

## SAP / ERP

Replace finance, inventory, procurement, and shipment methods with ERP APIs.

## Outlook / Microsoft Graph

Add tools for calendar, email, meeting context, and stakeholder communication. Require confirmation before sending messages.

## Teams

Add tools for channel search, meeting context, notifications, and approval workflows.

## Data platform

The tool layer can also query Snowflake, Databricks, BigQuery, PostgreSQL, or enterprise semantic layers.
