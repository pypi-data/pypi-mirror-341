import itertools
import logging
import os

from io import StringIO
from rich.tree import Tree
from rich import print as rich_print
from utilities_pufm.utils.enums import RichColors
from utilities_pufm.prints.logs import RichLogger, LogRedirector
from datetime import datetime
from rich.logging import RichHandler
from rich import box, print_json
from rich.align import Align
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn, MofNCompleteColumn, TimeRemainingColumn, TimeElapsedColumn
from rich.syntax import Syntax
from rich.table import Table

def custom_print_json(data):
    print_json(data=data)    

def print_matriz_bonita(df, nome: str = ""):
    console_terminal = Console()
    table = Table(title=f"Matriz de Similaridade entre Colunas - {nome}", box=box.ROUNDED, show_lines=True)

    table.add_column("↓ columns_to_drop / columns_to_add →", style="bold magenta", no_wrap=True)
    for col in df.columns:
        table.add_column(col, style="cyan", justify="center")

    for idx, row in df.iterrows():
        row_values = [f"{val:.1f}%" for val in row]
        table.add_row(idx, *row_values)

    buffer = StringIO()
    console = Console(file=buffer, force_terminal=True, width=140, no_color=True)
    console.print(table)
    console_terminal.print(table)
    
    return buffer.getvalue()

def custom_print(msg: str, rich: bool = True, colors: list = ["yellow"]):
    """
    Prints customized messages with optional styling using the Rich library.

    Args:
        msg (str): The message to display. 
                   To style parts of the text, use the '*' character as a delimiter.
                   For example, '*styled text*' will be displayed with special formatting.
        rich (bool): Determines whether the Rich library should be used for styling the output.
        colors (list): A list of colors to alternate for styling text segments 
                       enclosed by '*'. Colors should be strings and correspond to 
                       the `RichColors` enum.

    Example:
        custom_print("Normal text, *styled text*", rich=True, colors=["red", "blue"])

    Note:
        When using the Rich feature, the provided color names must be valid 
        according to the `RichColors` enum.
    """
    if rich:
        colors = itertools.cycle([RichColors[color.upper()].value for color in colors]) 
        first = True
        rich_msg = ""
        current_color = next(colors)
        for char in msg:
            if char == "*" and first:
                rich_msg += f"[bold {current_color}]"
                first = False
            elif char == "*":
                rich_msg += f"[/bold {current_color}]"
                first = True
                current_color = next(colors)
            else:
                rich_msg += char
                        
        rich_print(rich_msg)
        
    else:
        print(msg)

def custom_progress_bar(console: Console = None) -> Progress:
    """
    Creates and returns a custom progress bar using the Rich library.

    The progress bar includes:
        - A text column displaying the task description.
        - A text column showing the task completion percentage.
        - A bar column representing the progress visually.
        - A column showing the number of completed tasks out of the total tasks.
        - Time elapsed since the task started.
        - Estimated time remaining to complete the task.

    Returns:
        Progress: An instance of Rich's Progress class configured with the specified columns.
    """

    return Progress(
            TextColumn("[progress.description]{task.description}"), 
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            BarColumn(),
            MofNCompleteColumn(),
            TextColumn("•"),
            TimeElapsedColumn(),
            TextColumn("•"),
            TimeRemainingColumn(),
            console=console
        )

def print_directory_structure(directory="."):
    def build_tree(directory, tree):
        try:
            for entry in sorted(os.listdir(directory)):
                path = os.path.join(directory, entry)
                if os.path.isdir(path):
                    subtree = tree.add(f"[bold blue]📁 {entry}[/]")
                    build_tree(path, subtree)
                else:
                    tree.add(f"[green]📄 {entry}[/]")
        except PermissionError:
            tree.add("[red]⛔ Permission denied[/]")

    tree = Tree(f"[bold yellow]📂 {directory}[/]")
    build_tree(directory, tree)
    rich_print(tree)
    

class CustomRichLayout():
    FORMAT = '%(asctime)s'

    def __init__(self, name_layout, init_job_list, *args,**kwargs):
        self.name_layout = name_layout
        self.init_job_list = init_job_list
        self.log_message = []
        self.layout = None
        
        self.rl = RichLogger()
        self.lr = LogRedirector(update_log_func=self.rl.write)
        
        self.c = Console(file=self.rl, width=150)
        r = RichHandler(console=self.c)
        logging.basicConfig(
            level="NOTSET", format=self.FORMAT, datefmt="[%X]", handlers=[r]
        )
        self.logger = logging.getLogger("rich")
        
        self._define_layout()
        
    def _make_log_panel(self) -> Panel:
        """Some example content."""
        # log_message = Table.grid(padding=1)
        # log_message.add_column(style="green", justify="right")
        # log_message.add_column(no_wrap=True)
        log_text = '\n'.join(self.rl.messages)
        # log_message.add_row(f"{log_text}")
        
        # message = Table.grid(padding=1)
        # message.add_column()
        # message.add_column(no_wrap=True)
        # message.add_row(log_message)

        message_panel = Panel(
            Align.left(
                log_text,
                vertical="top",
            ),
            box=box.ROUNDED,
            padding=(1, 1),
            title="[b red]Log Messages",
            border_style="bright_blue",
        )
        return message_panel
    
    def update_log(self, message: str = ""):
        """Updates the log panel with a new message."""
        # self.log_message.append(message)
        self.layout["body"].update(self._make_log_panel())
    
    def _define_layout(self):
        def make_layout() -> Layout:
            """Define the layout."""
            layout = Layout(name="root")

            layout.split(
                Layout(name="header", size=3),
                Layout(name="main", ratio=1),
                Layout(name="footer", size=7),
            )
            layout["main"].split_row(
                Layout(name="side"),
                Layout(name="body", ratio=2, minimum_size=60),
            )
            layout["side"].split(
                Layout(name="box1"),
                Layout(name="box2")
            )
            return layout

        class Header:
            def __init__(self, name_layout):
                self.name_layout = name_layout
                
            def __rich__(self) -> Panel:
                grid = Table.grid(expand=True)
                grid.add_column(justify="center", ratio=1)
                grid.add_column(justify="right")
                grid.add_row(
                    f"{self.name_layout}",
                    datetime.now().ctime().replace(":", "[blink]:[/]"),
                )
                return Panel(grid, style="white on blue")

        def make_syntax() -> Syntax:
            code = """\
                print("Some msg for now")
            """
            syntax = Syntax(code, "python", line_numbers=True)
            return syntax

        self.job_progress = Progress(
            "{task.description}",
            SpinnerColumn(),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        )
        self.job_ids = {}
        for job_name, job_length, job_id in self.init_job_list:
            self.job_ids[job_id] = self.job_progress.add_task(job_name, total=job_length)
            
            # job_progress.add_task("[green]Cooking")
            # job_progress.add_task("[magenta]Baking", total=200)
            # job_progress.add_task("[cyan]Mixing", total=400)

        total = sum(task.total if task.total is not None else 0 for task in self.job_progress.tasks)
        self.overall_progress = Progress()
        overall_task = self.overall_progress.add_task("All Jobs", total=int(total))

        progress_table = Table.grid(expand=True)
        progress_table.add_row(
            Panel(
                self.overall_progress,
                title="Overall Progress",
                border_style="green",
                padding=(2, 2),
            ),
            Panel(self.job_progress, title="[b]Jobs", border_style="red", padding=(1, 2)),
        )

        self.layout = make_layout()
        self.layout["header"].update(Header(self.name_layout))
        self.layout["body"].update(self._make_log_panel())
        self.layout["box2"].update(Panel(make_syntax(), border_style="green"))
        self.layout["box1"].update(Panel(self.layout.tree, border_style="red"))
        self.layout["footer"].update(progress_table)

    def add_job(self, job_description, job_id, total=None):
        job_rich_id = self.job_progress.add_task(job_description, total=total)
        self.job_ids[job_id] = job_rich_id
       