import azure.functions as func
import logging

from Create_Order import Create_Order # Importing our blue print

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

# Register The Blue Print
app.register_functions(Create_Order)