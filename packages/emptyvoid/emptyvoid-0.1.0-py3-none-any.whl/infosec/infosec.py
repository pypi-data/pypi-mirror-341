import os

DOCX_FOLDER = os.path.join(os.path.dirname(__file__), '../docx_files')
PKT_FOLDER = os.path.join(os.path.dirname(__file__), '../pkt_files')

def list_docx_files():
    """List all .docx files in the docx_files directory."""
    return [f for f in os.listdir(DOCX_FOLDER) if f.endswith('.docx')]

def list_pkt_files():
    """List all .pkt files in the pkt_files directory."""
    return [f for f in os.listdir(PKT_FOLDER) if f.endswith('.pkt')]
