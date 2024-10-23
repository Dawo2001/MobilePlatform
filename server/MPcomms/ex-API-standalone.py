# --- --- --- --- --- --- --- --- --- --- --- --- ---
# Standalone api server
# --- --- --- --- --- --- --- --- --- --- --- --- ---

from RestAPI.server import restAP 

if __name__ == "__main__":
    print("Server started on address localhost:5000/api")
    print("Documentation accessible at http://localhost:5000/api/doc")
    restAP.run()
    
