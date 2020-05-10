fun addToString(n, string) = 
	if String.size(string) >= n
	then string
	else "0"^addToString(n-1,string)


fun calculateTimeStamp() = 
let
	val totalTime = IntInf.toInt(time()) * 60 *24

	(* calculating date *)
	(* Note: this is a rough approximation *)

	val oneYear = 365 * 24 * 60 (* 1 year = 365 days x 24 hours x 60 minutes *)
	val year = (totalTime div oneYear)+2006
	val restYear = totalTime mod oneYear

	(* The timestamp field allows for years from 0000 to 9999. Thus, we have to make sure we use a valid timestamp. *)
	val year = year mod 10000
	val stringYear = Int.toString(year)
	val stringYear = addToString(4, stringYear)

	val oneMonth = 31 * 24 * 60 (* 1 month = 31 days x 24 hours x 60 minutes *)
	val month = (restYear div oneMonth) + 1 
	val restMonth = restYear mod oneMonth
	
	val oneDay = 24 * 60  (* 1 day = 24 hours x 60 minutes *)
	val day = (restMonth div oneDay) + 1
	val restDay = restMonth mod oneDay


	(* The timestamp field allows for months from 01 to 12. Thus, we have to make sure we use a valid timestamp. *)
	(* Checking if it is February and change the date to 28 if the day is 29 or 30 *)
	val day = if month = 2 andalso day >= 29 then 29 else day

	val stringMonth = Int.toString(month)
	val stringMonth = addToString(2, stringMonth)



	(* The timestamp field allows for days from 01 to 31. Thus, we have to make sure we use a valid timestamp. *)
	val stringDay = Int.toString(day)
	val stringDay = addToString(2, stringDay)

	(* calcultating time *)

	val hours = restDay div 60
	val stringHours = Int.toString(hours)
	val stringHours = addToString(2, stringHours)

	val minutes = restDay mod 60
	val stringMinutes = Int.toString(minutes)
	val stringMinutes = addToString(2, stringMinutes)


	val timestamp = stringYear^"-"^stringMonth^"-"^stringDay^"T"^stringHours^":"^stringMinutes^":"^"00.000+01:00"

in
	timestamp
end;




fun writeTimeStamp(file_id, timestamp) = 
let
	val _ = TextIO.output(file_id, "<Timestamp>")
	val _ = TextIO.output(file_id, timestamp)


in
	TextIO.output(file_id, "</Timestamp>\n")
end;



fun writeWorkflowModelElement(file_id, workflowModelElement) = 
let
	val _ = TextIO.output(file_id, "<WorkflowModelElement>")
	val _ = TextIO.output(file_id, workflowModelElement)


in
	TextIO.output(file_id, "</WorkflowModelElement>\n")
end;


fun getDescription(description) = 
	if length(description) = 0
	then ""
	else hd(description)


fun getComplement(event, description) = 
let
	val desc = getDescription(description)
	val complement = "unknowntype=\"" ^ desc ^ "\""
in
	if event = "unknown"
	then  complement
	else  ""
end;


fun writeEventType(file_id, event :: description) = 
let

	val complement = getComplement(event, description)
	val _ = TextIO.output(file_id, "<EventType ")
	val _ = TextIO.output(file_id, complement)
	val _ = TextIO.output(file_id, ">")		
	val _ = TextIO.output(file_id, event)

in
	TextIO.output(file_id, "</EventType>\n")
end;



fun writeOriginator(file_id, Originator) = 
let
	val _ = TextIO.output(file_id, "<Originator>")
	val _ = TextIO.output(file_id, Originator)

in
	TextIO.output(file_id, "</Originator>\n")
end;


fun writeDataAttributes(nil) = " "
| writeDataAttributes(name::nil) =  "<Attribute name = \"" ^ name ^ "\"> </Attribute>\n" 
| writeDataAttributes(name::value::tail) = "<Attribute name = \"" ^ name ^ "\">" ^value ^" </Attribute>\n" ^ writeDataAttributes(tail) 

fun writeData(file_id, data) = 
let
	val _ = TextIO.output(file_id, "<Data>")
	val _ = TextIO.output(file_id, writeDataAttributes(data))
in
	TextIO.output(file_id, "</Data>")
end;	  

fun  testWriteData (file_id, data) = 
	if length(data) = 0
	then TextIO.output(file_id, "")
	else writeData(file_id, data)

fun add (file_id, workflowModelElement, EventType, TimeStamp, Originator, Data)=
let
	val _ = TextIO.output(file_id, "<AuditTrailEntry>\n")
	val _ = testWriteData(file_id, Data)
	val _ = writeWorkflowModelElement(file_id, workflowModelElement)
	val _ = writeEventType(file_id, EventType)
	val _ = writeTimeStamp(file_id, TimeStamp)
	val _ = writeOriginator(file_id, Originator)
	val _ = TextIO.output(file_id, "</AuditTrailEntry>\n")

in
	TextIO.closeOut(file_id)
end;



fun addATE (caseID,workflowModelElement, EventType, TimeStamp, Originator, Data) = 
let
	val file_id = TextIO.openAppend(FILE^Int.toString(caseID)^FILE_EXTENSION)
in
	add(file_id, workflowModelElement, EventType, TimeStamp, Originator, Data)
end;

fun createCaseFile(caseID) = 
let
   val caseIDString = Int.toString(caseID)
   val file_id = TextIO.openOut(FILE ^ caseIDString  ^ FILE_EXTENSION)
   val _ = TextIO.output(file_id, caseIDString  ^ "\n")
in
   TextIO.closeOut(file_id)
end;


