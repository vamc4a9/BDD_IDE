package GUI;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

public class FindStepDef {

	public List<List<String>> FindMatch(String sXMLPath, String sStatement, String sParameters) {
		String[] sParams = sParameters.split("\n");
		for (String param : sParams) {
			if (param.contains("==")) {
				String[] arParam = param.split("==");
				sStatement = sStatement.replace(arParam[0], "");
			}
		}
		
		String[] sWords = sStatement.split(" ");
		Map<String, List<String>> sOutput = new HashMap<String, List<String>>();
		for (String word : sWords) {
			if ((!sOutput.containsKey(word)) && (!word.trim().contentEquals(""))) {
				xml oXML = new xml();
				sOutput.put(word, oXML.fn_FindInXml(sXMLPath, "//StepDefinition[contains(@Statement,'" + word + "')]/@Statement"));
			}
		}
		
		int MaxMatches;
		if (sOutput.size() < 3)
			MaxMatches = sOutput.size();
		else if (sOutput.size() < 5)
			MaxMatches = sOutput.size() - 1;
		else
			MaxMatches = sOutput.size() - 3;
		
		List<String> tempOutput = new ArrayList<String>();
		List<List<String>> rOutput = new ArrayList<List<String>>();
		Set<String> sKeyset = sOutput.keySet();
		for (String key : sKeyset) {
			List<String> lList = sOutput.get(key);
			for (String string : lList) {
				if (fn_FindMatchCount(string.split("::")[1], sOutput) >= MaxMatches) {
					List<String> tempList = new ArrayList<String>();
					if (!tempOutput.contains(string)) {
						tempOutput.add(string);
						tempList.add(string.split("::")[0]);
						tempList.add(string.split("::")[1]);
						rOutput.add(tempList);
					}
				}
			}
		}
		
		return rOutput;
	}
	
	public Integer fn_FindMatchCount(String sStatement, Map<String, List<String>> sOutput) {
		int iMatch = 0;
		Set<String> sKeyset = sOutput.keySet();
		for (String key : sKeyset) {
			List<String> lList = sOutput.get(key);
			for (String string : lList) {
				if (string.split("::")[1].contentEquals(sStatement)) {
					iMatch++;
				}
			}
		}
		return iMatch;
	}
	
}
