terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }
}

provider "azurerm" {
  features {}
  subscription_id = "71406c77-43f9-4b7b-9a73-bd27ca9881cf"
}

resource "azurerm_resource_group" "rg" {
  name     = "bfwithmaja-rg"
  location = "Poland Central"
}

resource "azurerm_service_plan" "plan" {
  name                = "bfwithmaja-plan"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  os_type             = "Linux"
  sku_name            = "F1"
}

resource "azurerm_linux_web_app" "app" {
  name                = "bfwithmaja-tf"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  service_plan_id     = azurerm_service_plan.plan.id

   site_config {
    always_on        = false
    app_command_line = "gunicorn --bind=0.0.0.0 app:app"

    application_stack {
      python_version = "3.11"
    }
  }
}

output "app_url" {
  value = "https://${azurerm_linux_web_app.app.default_hostname}"
}
