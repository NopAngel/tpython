with Ada.Text_IO; use Ada.Text_IO;
with Ada.Strings.Unbounded; use Ada.Strings.Unbounded;
with Ada.Command_Line; use Ada.Command_Line;
with GNAT.OS_Lib; use GNAT.OS_Lib;
with Ada.Directories; use Ada.Directories;

package Python_Testing is
    type Test_Result is (PASS, FAIL, ERROR);
    type Test_Case is record
        Name : Unbounded_String;
        Result : Test_Result;
        Message : Unbounded_String;
        Duration : Duration;
    end record;
    
    procedure Run_Test_Suite(Directory : String);
    procedure Analyze_Python_Code(File_Path : String);
    function Check_Python_Syntax(File_Path : String) return Boolean;
    procedure Generate_Test_Report;
end Python_Testing;

package body Python_Testing is
    Total_Tests : Natural := 0;
    Passed_Tests : Natural := 0;
    Failed_Tests : Natural := 0;
    Test_Results : Unbounded_String := To_Unbounded_String("");
    
    function Execute_Python_Command(Command : String) return Integer is
        Args : Argument_List := (1 => new String'("-c"), 2 => new String'(Command));
        Success : Boolean;
    begin
        return GNAT.OS_Lib.Spawn(Program_Name => "python3", Args => Args, Success => Success);
    end Execute_Python_Command;
    
    function Run_Python_Test(Test_File : String) return Test_Case is
        Result : Test_Case;
        Start_Time : Time;
        End_Time : Time;
        Exit_Code : Integer;
    begin
        Result.Name := To_Unbounded_String(Test_File);
        Start_Time := Clock;
        Exit_Code := Execute_Python_Command("exec(open('" & Test_File & "').read())");
        End_Time := Clock;
        Result.Duration := End_Time - Start_Time;
        
        if Exit_Code = 0 then
            Result.Result := PASS;
            Result.Message := To_Unbounded_String("Test passed");
            Passed_Tests := Passed_Tests + 1;
        else
            Result.Result := FAIL;
            Result.Message := To_Unbounded_String("Test failed code" & Integer'Image(Exit_Code));
            Failed_Tests := Failed_Tests + 1;
        end if;
        
        Total_Tests := Total_Tests + 1;
        return Result;
    end Run_Python_Test;
    
    procedure Run_Test_Suite(Directory : String) is
        Search : Search_Type;
        Dir_Entry : Directory_Entry_Type;
    begin
        Put_Line("Testing Python Suite: " & Directory);
        Put_Line("==================================================");
        
        Start_Search(Search, Directory, "*.py");
        
        while More_Entries(Search) loop
            Get_Next_Entry(Search, Dir_Entry);
            if Simple_Name(Dir_Entry) /= "__init__.py" then
                declare
                    File_Path : constant String := Full_Name(Dir_Entry);
                    Test_Result : Test_Case;
                begin
                    Test_Result := Run_Python_Test(File_Path);
                    
                    Append(Test_Results, "Test: " & To_String(Test_Result.Name) & ASCII.LF);
                    Append(Test_Results, "Result: " & Test_Result'Image(Test_Result.Result) & ASCII.LF);
                    Append(Test_Results, "Duration: " & Duration'Image(Test_Result.Duration) & "s" & ASCII.LF);
                    Append(Test_Results, "Message: " & To_String(Test_Result.Message) & ASCII.LF);
                    Append(Test_Results, "---" & ASCII.LF);
                    
                    Put(Simple_Name(Dir_Entry) & " ... ");
                    case Test_Result.Result is
                        when PASS => Put_Line("PASS");
                        when FAIL => Put_Line("FAIL");
                        when ERROR => Put_Line("ERROR");
                    end case;
                end;
            end if;
        end loop;
        
        End_Search(Search);
    end Run_Test_Suite;
    
    procedure Analyze_Python_Code(File_Path : String) is
    begin
        Put_Line("Analyzing: " & File_Path);
        
        if Check_Python_Syntax(File_Path) then
            Put_Line("  Syntax: VALID");
        else
            Put_Line("  Syntax: INVALID");
        end if;
        
        Execute_Python_Command(
            "import ast; " &
            "try: " &
            "    with open('" & File_Path & "', 'r') as f: " &
            "        tree = ast.parse(f.read()); " &
            "    print('  AST: PARSABLE'); " &
            "    print('  Functions:', sum(1 for node in ast.walk(tree) if isinstance(node, ast.FunctionDef))); " &
            "    print('  Classes:', sum(1 for node in ast.walk(tree) if isinstance(node, ast.ClassDef))); " &
            "except Exception as e: " &
            "    print('  AST Error:', str(e))"
        );
    end Analyze_Python_Code;
    
    function Check_Python_Syntax(File_Path : String) return Boolean is
        Exit_Code : Integer;
    begin
        Exit_Code := Execute_Python_Command(
            "try: " &
            "    compile(open('" & File_Path & "').read(), '" & File_Path & "', 'exec'); " &
            "    exit(0); " &
            "except SyntaxError: " &
            "    exit(1)"
        );
        
        return Exit_Code = 0;
    end Check_Python_Syntax;
    
    procedure Generate_Test_Report is
        Report_File : File_Type;
    begin
        Put_Line("TEST REPORT");
        Put_Line("==================================================");
        Put_Line("Total Tests: " & Natural'Image(Total_Tests));
        Put_Line("Passed: " & Natural'Image(Passed_Tests));
        Put_Line("Failed: " & Natural'Image(Failed_Tests));
        
        if Total_Tests > 0 then
            Put_Line("Success Rate: " & 
                    Integer'Image((Passed_Tests * 100) / Total_Tests) & "%");
        end if;
        
        Create(Report_File, Out_File, "python_test_report.txt");
        Put_Line(Report_File, "Python Test Report");
        Put_Line(Report_File, "Total Tests: " & Natural'Image(Total_Tests));
        Put_Line(Report_File, "Passed: " & Natural'Image(Passed_Tests));
        Put_Line(Report_File, "Failed: " & Natural'Image(Failed_Tests));
        Put_Line(Report_File, To_String(Test_Results));
        Close(Report_File);
        
        Put_Line("Report saved: python_test_report.txt");
    end Generate_Test_Report;

end Python_Testing;

with Python_Testing; use Python_Testing;

procedure Test_Main is
begin
    if Argument_Count = 0 then
        Put_Line("Usage: test_main <directory>");
        return;
    end if;
    
    Run_Test_Suite(Argument(1));
    Generate_Test_Report;
    
    Put_Line("Testing completed.");
end Test_Main;
