from core import BaseCommand

class GreetCommand(BaseCommand):
    name = "greet"
    help = "Say hellp to someone."
    
    def configure(self, parser):
        parser.add_argument("--name", required=True, help="Name of the person")
        
    def run(self, args):
        print(f"Hello, {args.name}!")