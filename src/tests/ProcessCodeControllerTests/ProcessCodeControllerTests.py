import json
import unittest

from controllers.ProcessCodeController import ProcessCodeController


class ProcessCodeControllerTests(unittest.TestCase):
    """
    Tests to check if new changes don't break anything already working.
    Those are functional tests, checking only the output
    """

    def test_multiple_variable_declaration_initialization_separated(self):
        data = json.loads(r"""{"code":"int test(void){pid_t pid, pid2; pid = fork(); write(2, 1, 21); return (1);}",
        "generalizeFunctionNames":true,"returnType":0,
        "generalizeVariableNames":true,
        "generalizeStrings":true,
        "replacementStrategy":0,
        "tryRecoverFromErrors":false}""")
        controller = ProcessCodeController()
        out = " ".join( controller.processCode(data))

        self.assertEqual(out, "int FUNC0 ( void ) { pid_t VAR0 , VAR1 ; VAR0 = fork ( ) ; write ( 2 , 1 , 21 ) ; return ( 1 ) ; } <EOF>")  # add assertion here

    def test_multiple_variable_declaration_initialization_separated_NO_VAR_GENERALIZED(self):
        data = json.loads(r"""{"code":"int test(void){pid_t pid, pid2; pid = fork(); write(2, 1, 21); return (1);}",
        "generalizeFunctionNames":true,"returnType":0,
        "generalizeVariableNames":false,
        "generalizeStrings":true,"replacementStrategy":0,"tryRecoverFromErrors":false}""")
        controller = ProcessCodeController()
        out = " ".join( controller.processCode(data))

        self.assertEqual(out, "int FUNC0 ( void ) { pid_t pid , pid2 ; pid = fork ( ) ; write ( 2 , 1 , 21 ) ; return ( 1 ) ; } <EOF>")  # add assertion here

    def test_multiple_variable_declaration_initialization_separated_NO_FUNC_GENERALIZED(self):
        data = json.loads(r"""{"code":"int test(void){pid_t pid, pid2; pid = fork(); write(2, 1, 21); return (1);}",
        "generalizeFunctionNames":false,
        "returnType":0,
        "generalizeVariableNames":true,
        "generalizeStrings":true,"replacementStrategy":0,"tryRecoverFromErrors":false}""")
        controller = ProcessCodeController()
        out = " ".join( controller.processCode(data))

        self.assertEqual(out, "int test ( void ) { pid_t VAR0 , VAR1 ; VAR0 = fork ( ) ; write ( 2 , 1 , 21 ) ; return ( 1 ) ; } <EOF>")  # add assertion here

    def test_multiple_variable_declaration_initialization_separated_NO_FUNC_VAR_GENERALIZED(self):
        data = json.loads(r"""{"code":"int test(void){pid_t pid, pid2; pid = fork(); write(2, 1, 21); return (1);}",
        "generalizeFunctionNames":false,
        "returnType":0,
        "generalizeVariableNames":false,
        "generalizeStrings":true,"replacementStrategy":0,"tryRecoverFromErrors":false}""")
        controller = ProcessCodeController()
        out = " ".join( controller.processCode(data))

        self.assertEqual(out, "int test ( void ) { pid_t pid , pid2 ; pid = fork ( ) ; write ( 2 , 1 , 21 ) ; return ( 1 ) ; } <EOF>")  # add assertion here

    def test_single_variable_declaration_initialization_separated(self):
        data = json.loads(r"""{"code":"int test2(void){pid_t pid; pid = fork(); write(2, 1, 21); return (1);}",
        "generalizeFunctionNames":true,"returnType":0,
        "generalizeVariableNames":true,
        "generalizeStrings":true,"replacementStrategy":0,"tryRecoverFromErrors":false}""")
        controller = ProcessCodeController()
        out = " ".join( controller.processCode(data))
        self.assertEqual(out, "int FUNC0 ( void ) { pid_t VAR0 ; VAR0 = fork ( ) ; write ( 2 , 1 , 21 ) ; return ( 1 ) ; } <EOF>")  # add assertion here

    def test_single_variable_declaration_initialization_separated_NO_VAR_GENERALIZED(self):
        data = json.loads(r"""{"code":"int test2(void){pid_t pid; pid = fork(); write(2, 1, 21); return (1);}",
        "generalizeFunctionNames":true,"returnType":0,
        "generalizeVariableNames":false,
        "generalizeStrings":true,"replacementStrategy":0,"tryRecoverFromErrors":false}""")
        controller = ProcessCodeController()
        out = " ".join( controller.processCode(data))
        self.assertEqual(out, "int FUNC0 ( void ) { pid_t pid ; pid = fork ( ) ; write ( 2 , 1 , 21 ) ; return ( 1 ) ; } <EOF>")  # add assertion here

    def test_single_variable_declaration_initialization_separated_NO_FUNC_GENERALIZED(self):
        data = json.loads(r"""{"code":"int test2(void){pid_t pid; pid = fork(); write(2, 1, 21); return (1);}",
        "generalizeFunctionNames":false,
        "returnType":0,
        "generalizeVariableNames":true,
        "generalizeStrings":true,"replacementStrategy":0,"tryRecoverFromErrors":false}""")
        controller = ProcessCodeController()
        out = " ".join( controller.processCode(data))
        self.assertEqual(out, "int test2 ( void ) { pid_t VAR0 ; VAR0 = fork ( ) ; write ( 2 , 1 , 21 ) ; return ( 1 ) ; } <EOF>")  # add assertion here

    def test_single_variable_declaration_initialization_separated_NO_VAR_FUNC_GENERALIZED(self):
        data = json.loads(r"""{"code":"int test2(void){pid_t pid; pid = fork(); write(2, 1, 21); return (1);}",
        "generalizeFunctionNames":false,
        "returnType":0,
        "generalizeVariableNames":false,
        "generalizeStrings":true,"replacementStrategy":0,"tryRecoverFromErrors":false}""")
        controller = ProcessCodeController()
        out = " ".join( controller.processCode(data))
        self.assertEqual(out, "int test2 ( void ) { pid_t pid ; pid = fork ( ) ; write ( 2 , 1 , 21 ) ; return ( 1 ) ; } <EOF>")  # add assertion here

    def test_single_variable_declaration_initialization_separated_function_usage(self):
        data = json.loads("""{
            "code": "int test2(void){pid_t pid; pid = fork(); printf(\\"O pid e: %d\\", pid); return (1);}",
            "generalizeFunctionNames": true,
            "returnType":0,
            "generalizeVariableNames": true,
            "generalizeStrings":true,"replacementStrategy":0,"tryRecoverFromErrors":false}""")
        controller = ProcessCodeController()
        out = " ".join( controller.processCode(data))
        self.assertEqual(out, "int FUNC0 ( void ) { pid_t VAR0 ; VAR0 = fork ( ) ; printf ( STRING_TOKEN , VAR0 ) ; return ( 1 ) ; } <EOF>")  # add assertion here

    def test_single_variable_declaration_initialization_separated_point_initialization_function_usage(self):
        data = json.loads("""{
            "code": "int test2(void){int* pid; *pid = fork(); printf(\\"O pid e: %d\\", *pid); return (1);}",
            "generalizeFunctionNames": true,
            "returnType":0,
            "generalizeVariableNames": true,
            "generalizeStrings":true,"replacementStrategy":0,"tryRecoverFromErrors":false}""")
        controller = ProcessCodeController()
        out = " ".join( controller.processCode(data))
        self.assertEqual(out, "int FUNC0 ( void ) { int * VAR0 ; * VAR0 = fork ( ) ; printf ( STRING_TOKEN , * VAR0 ) ; return ( 1 ) ; } <EOF>")  # add assertion here

    def test_single_variable_declaration_initialization_separated_point_initialization_function_usage_minify(self):
        data = json.loads("""{
            "code": "int test2(void){int* pid; *pid = fork(); printf(\\"O pid e: %d\\", *pid); return (1);}",
            "generalizeFunctionNames": true,
            "returnType":0,
            "generalizeVariableNames": true,
            "generalizeStrings":true,"replacementStrategy":1,"tryRecoverFromErrors":false}""")
        controller = ProcessCodeController()
        out = " ".join( controller.processCode(data))
        self.assertEqual(out, "int a ( void ) { int * b ; * b = fork ( ) ; printf ( S , * b ) ; return ( 1 ) ; } <EOF>")  # add assertion here

    def test_replacement_strings_minify(self):
        data = json.loads(r"""{
            "code": "int test2(void){int* pid; *pid = fork(); printf(\"O pid e: %d\", *pid); char a = 'o'; return (1);}",
            "generalizeFunctionNames": true,
            "returnType":1,
            "generalizeVariableNames": true,
            "generalizeStrings":true,"replacementStrategy":1,"tryRecoverFromErrors":false}""")
        controller = ProcessCodeController()
        out =  controller.processCode(data)
        self.assertEqual("int a(void){int* b; *b = fork(); printf(S, *b); char c = S; return (1);}", out)

    def test_minify_without_string_replacement(self):

        data = json.loads(r"""{
            "code": "int test2(void){int* pid; *pid = fork(); printf(\"O pid e: %d\", *pid); char a = 'o'; return (1);}",
            "generalizeFunctionNames": true,
            "returnType":1,
            "generalizeVariableNames": true,
            "generalizeStrings":false,"replacementStrategy":1,"tryRecoverFromErrors":false}""")
        controller = ProcessCodeController()
        out =  controller.processCode(data)
        self.assertEqual("int a(void){int* b; *b = fork(); printf(\"O b e: %d\", *b); char c = 'o'; return (1);}", out)

    def test_minify_var_replacement_v2(self):
        data = json.loads(r"""{
               "code": "int test2(int teste1, int teste2){int* pid; *pid = fork(); printf(\"O pid e: %d\", *pid); char teste[] = 'o'; return (1);}",
               "generalizeFunctionNames": true,
               "returnType":1,
               "generalizeVariableNames": true,
               "generalizeStrings":false,"replacementStrategy":1,"tryRecoverFromErrors":false}""")
        controller = ProcessCodeController()
        out = controller.processCode(data)
        self.assertEqual("int a(int b, int c){int* d; *d = fork(); printf(\"O d e: %d\", *d); char e[] = 'o'; return (1);}", out)
    def test_minify_string_replacement_multiple_one_line(self):
        data = json.loads(r"""{
               "code": "int test2(int teste1, int teste2){int* pid; *pid = fork(); char ola[] = \"teste\"; printf(\"O pid e: %d\", *pid); char teste3[] = 'o'; return (1);}",
               "generalizeFunctionNames": true,
               "returnType":1,
               "generalizeVariableNames": true,
               "generalizeStrings":false,"replacementStrategy":1,"tryRecoverFromErrors":false}""")
        controller = ProcessCodeController()
        out = controller.processCode(data)
        self.assertEqual("int a(int b, int c){int* d; *d = fork(); char e[] = \"teste\"; printf(\"O d e: %d\", *d); char f[] = 'o'; return (1);}", out)

    def test_minify_recursive(self):
        data = json.loads(r"""{
                  "code": "int test2(int teste1, int teste2){ if(teste1 == 10){ teste1 = teste1 + 1; test2(teste1,teste2+teste1);} return teste2; }",
                  "generalizeFunctionNames": true,
                  "returnType":1,
                  "generalizeVariableNames": true,
                  "generalizeStrings":false,"replacementStrategy":1,"tryRecoverFromErrors":false}""")
        controller = ProcessCodeController()
        out = controller.processCode(data)
        self.assertEqual(
            "int a(int b, int c){ if(b == 10){ b = b + 1; a(b,c+b);} return c; }",
            out)
    def test_decl_func_2(self):
        data = json.loads(r"""{
                  "code": "test2(teste1, teste3)(int pivete){ if(teste1 == 10){ teste1 = teste1 + 1; test2(teste1,teste3+teste1);} return teste3; }",
                  "generalizeFunctionNames": true,
                  "returnType":1,
                  "generalizeVariableNames": true,
                  "generalizeStrings":false,"replacementStrategy":1,"tryRecoverFromErrors":false}""")
        controller = ProcessCodeController()
        out = controller.processCode(data)
        self.assertEqual(
            "a(teste1, teste3)(int b){ if(teste1 == 10){ teste1 = teste1 + 1; a(teste1,teste3+teste1);} return teste3; }",
            out)
    def test_decl_func_3(self):
        data = json.loads(r"""{
                  "code": "void FullFramePixelBuffer::setBuffer(int width, int height,rdr::U8* data_, int stride_){  if ((width < 0) || (width > maxPixelBufferWidth))    throw rfb::Exception(\"asd\", width); ModifiablePixelBuffer::setSize(width, height);  stride = stride_;  data = data_;}",
                  "generalizeFunctionNames": true,
                  "returnType":1,
                  "generalizeVariableNames": true,
                  "generalizeStrings":false,"replacementStrategy":1,"tryRecoverFromErrors":false}""")
        controller = ProcessCodeController()
        out = controller.processCode(data)

        self.assertEqual(
            "void FullFramePixelBuffer::a(int g, int h,rdr::U8* d, int e){ if ((g < 0) || (g > maxPixelBufferWidth)) throw rfb::Exception(\"asd\", g); ModifiablePixelBuffer::f(g, h); stride = e; data = d;}",
            out)
    def test_decl_func_4(self):
        data = json.loads(r"""{
                  "code": "void LineBitmapRequester::ReconstructRegion(const RectAngle<LONG> &orgregion,const struct RectangleRequest *rr){ printf(\"test!\");}",
                  "generalizeFunctionNames": true,
                  "returnType":1,
                  "generalizeVariableNames": true,
                  "generalizeStrings":true,"replacementStrategy":1,"tryRecoverFromErrors":false}""")
        controller = ProcessCodeController()
        out = controller.processCode(data)

        self.assertEqual(
            "void LineBitmapRequester::a(const RectAngle<LONG> &b,const struct RectangleRequest *c){ printf(S);}",
            out)
if __name__ == '__main__':
    unittest.main()
