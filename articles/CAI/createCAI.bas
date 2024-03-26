Attribute VB_Name = "createCAI"
    Dim form1 As UserForm1
    Dim CAI As CAI
Const PROBLEMSHEET = "TOEIC Part5"
Sub start()

    Sheets(PROBLEMSHEET).Visible = False
    Set CAI = New CAI
    Set form1 = New UserForm1

    Call show_question(True)
    
End Sub

Sub show_question(first As Boolean)
    form1.LblQuestion = CAI.get_next_question()
    form1.lblOption1 = CAI.get_ith_option(1)
    form1.lblOption2 = CAI.get_ith_option(2)
    form1.lblOption3 = CAI.get_ith_option(3)
    form1.lblOption4 = CAI.get_ith_option(4)
    form1.lblExplanation = ""
    form1.lblResult = ""
    form1.correctAnswer = CAI.get_correct_answer_number()
    form1.correctAnswerStr = CAI.get_answer()
    form1.explanationStr = CAI.get_explanation()
    If first Then
        form1.Show
    Else
        form1.Repaint
    End If
End Sub

Sub next_question()
    Dim CAI As CAI
    Set CAI = New CAI

    Debug.Print (" " & CAI.get_next_question())
    Debug.Print (CAI.get_options())
    Debug.Print (CAI.get_answer())
    
End Sub




Sub run_debug()
    Dim CAI As CAI
    Set CAI = New CAI
    Debug.Print ("stated..")
    Call CAI.debug_last_line
    Call CAI.debug_random
    
End Sub
