VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "CAI"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Base 1
Const questionColumn = 1
Const explanationColumn = 2
Const option1Column = 3
Const option2Column = 4
Const option3Column = 5
Const option4Column = 6


Private currentSheet As String

Private currentLine As Long
Private correctAnswer As String
Private optionArray(4) As Long
Private lastLine As Long
Private alphabet(4) As String
Private Sub set_last_line()
    lastLine = Sheets(currentSheet).Cells(Rows.count, 1).End(xlUp).row
End Sub

Public Sub debug_last_line()
    Debug.Print ("last line is " & lastLine)
End Sub

Public Sub debug_random()
    Dim i As Long
    Dim n As Long
    Dim count(lastLine) As Long
    Dim error As Long
    error = 0
    For i = 0 To 100000
        Call set_next_question
        count(currentLine) = count(currentLine) + 1
        If currentLine < 2 Then
            Debug.Print ("error!!! line is out of scope. line is" & currentLine)
            error = error + 1
        End If
        If currentLine > lastLine Then
            Debug.Print ("error!! line is out of scope. line is" & currentLine)
            error = error + 1
        End If
        
    Next i

    If error = 0 Then
        Debug.Print ("tried " & i & " times and found no error")
    End If
    For n = 2 To lastLine
        If count(n) = 0 Then
            
            Debug.Print ("tried " & i & "times but " & n & " never occured")
        End If
    Next n
End Sub
Private Function get_how_many_questions() As Long
    get_how_many_questions = lastLine - 1
    
End Function
Private Sub set_next_question()
    currentLine = (lastLine - 2) * Rnd + 2
End Sub

Public Function get_next_question() As String
    Call set_next_question
    Call randomize_option_array
    With Sheets(currentSheet)
        get_next_question = .Cells(currentLine, questionColumn).Value
        correctAnswer = .Cells(currentLine, option1Column).Value
    End With
End Function

Public Function get_explanation() As String
    get_explanation = Sheets(currentSheet).Cells(currentLine, explanationColumn).Value
End Function
Public Sub dump_option_array()
    Dim i As Long
    For i = 1 To 4
        Debug.Print (" " & i & " ==> " & optionArray(i))
    Next i
End Sub

Public Function get_answer() As String
    get_answer = alphabet(get_correct_answer_number()) & ". " & correctAnswer
    
End Function
Public Function get_correct_answer_number()
    Dim i As Long
    For i = 1 To 4
        If optionArray(i) = 1 Then
            get_correct_answer_number = i
            Exit Function
        End If
    Next i
    get_correct_answer_number = 0 'error
End Function
Private Sub set_current_sheet()
    currentSheet = "TOEIC Part5"
End Sub

Private Sub swap(ByRef a As Long, ByRef b As Long)
    Dim work As Long
    work = a
    a = b
    b = work
End Sub

Private Sub initialize_option_array()
    Dim i As Long
    For i = 1 To 4
        optionArray(i) = i
    Next i
End Sub

Private Sub initialize_alphabet()
    alphabet(1) = "A"
    alphabet(2) = "B"
    alphabet(3) = "C"
    alphabet(4) = "D"
End Sub

Private Sub Class_Initialize()
    Randomize
    Call set_current_sheet
    Call initialize_option_array
    Call set_last_line
    Call initialize_alphabet
End Sub

Private Sub randomize_option_array()
    Const numSwap = 8
    Dim randomNumber As Long
    Dim i As Long
    For i = 1 To numSwap
        randomNumber = 2 * Rnd + 2 'one of 2,3,4
        Call swap(optionArray(1), optionArray(randomNumber))
    Next i
End Sub

Public Function get_options() As String
    Dim i As Long
    get_options = ""
    For i = 1 To 4
        get_options = get_options & alphabet(i) & ". " & get_ith_option(optionArray(i)) & vbCrLf
    Next i
End Function
Public Function get_ith_option(i As Long) As String

    
    Select Case optionArray(i)
        Case 1
            get_ith_option = Sheets(currentSheet).Cells(currentLine, option1Column).Value
        Case 2
            get_ith_option = Sheets(currentSheet).Cells(currentLine, option2Column).Value
        Case 3
            get_ith_option = Sheets(currentSheet).Cells(currentLine, option3Column).Value
        Case 4
            get_ith_option = Sheets(currentSheet).Cells(currentLine, option4Column).Value
    End Select
End Function

