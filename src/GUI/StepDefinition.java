package GUI;

import javax.swing.*;
import javax.swing.border.Border;

import java.awt.*; 
import java.awt.event.*; 

class StepDefinition 
	extends JFrame 
	implements ActionListener { 

	private Container c; 
	private JLabel title; 
	private JLabel statement; 
	private JTextField tname; 
	private JLabel ExternalData; 
	private JRadioButton yes; 
	private JRadioButton no; 
	private ButtonGroup datagp; 
	private JLabel category; 
	private JComboBox StepType; 
	private JLabel add; 
	private JTextArea tadd; 
	private JButton sub;
	private JButton update;
	private JButton delete;
	private JButton reset; 
	private JTextArea tout; 
	private JLabel res; 
	private JTextArea resadd; 
	private String sXMLPath, sExistingXpath;

	private String categoryList[] 
		= { "WebEdit", "WebList", "DataBase", "Browser", 
			"WebElement", "WebTable", "Auxillary", "Custom"}; 

	public StepDefinition(String sPath) 
	{ 
		sXMLPath = sPath;
		setFrame("Step Definition");

		c = getContentPane(); 
		c.setLayout(null); 
		
		Color TAborderColor = new Color(77, 166, 255);
		Color BtnBorderColor = new Color(255, 102, 0);
		Color RadioBtnBackGround = new Color(255, 255, 230);

		title = fn_AddTextLabel("Add Step Definition", "Arial", 20, new Dimension(300, 30), new Point(350, 30));
		statement = fn_AddTextLabel("Statement", "Arial", 15, new Dimension(200, 20), new Point(100,100));
		tname = fn_AddTextField("Arial", 15, new Dimension(270, 20), new Point(200, 100), TAborderColor, "");
		ExternalData = fn_AddTextLabel("Data Table?", "Arial", 15, new Dimension(100, 20), new Point(100, 150));
		yes = fn_AddRadioButton("Yes", "Arial", 15, new Dimension(75, 20), new Point(200, 150), true, RadioBtnBackGround);
		no = fn_AddRadioButton("No", "Arial", 15, new Dimension(75, 20), new Point(275, 150), false, RadioBtnBackGround);

		datagp = new ButtonGroup(); 
		datagp.add(yes);
		datagp.add(no);

		category = fn_AddTextLabel("Category", "Arial", 15, new Dimension(100, 20), new Point(100, 200));
		StepType = fn_AddComboBox(categoryList, "Arial", 15, new Dimension(90, 20), new Point(200, 200));
		
		fn_AddTextLabel("Parameters", "Arial", 15, new Dimension(100, 20), new Point(100, 250));
		fn_AddTextArea("Arial", 13, new Dimension(270, 40), new Point(200, 250),true, true, TAborderColor);
		
		add = fn_AddTextLabel("Instructions", "Arial", 15, new Dimension(100, 20), new Point(100, 300));
		tadd = fn_AddTextArea("Arial", 13, new Dimension(270, 200), new Point(200, 300),true, true, TAborderColor);
		sub = fn_AddButton("Submit", "Arial", 15, new Dimension(100, 20), new Point(300, 525),BtnBorderColor);
		reset = fn_AddButton("Reset", "Arial", 15, new Dimension(100, 20), new Point(450, 525),BtnBorderColor);
		tout = fn_AddTextArea("Arial", 15, new Dimension(300,400), new Point(500,100),true, false, TAborderColor);
		res = fn_AddTextLabel("", "Arial", 20, new Dimension(500, 25), new Point(100, 500));
		resadd = fn_AddTextArea("Arial", 13, new Dimension(200, 75), new Point(580, 175),true, true, TAborderColor);

		setVisible(true); 
	} 
	
	public StepDefinition(String sPath, String Statement, String xPath) 
	{ 
		sXMLPath = sPath;
		sExistingXpath = xPath + "/StepDefinition[@Statement='" + Statement + "']";
		xml oXml = new xml();
		String sExternalData = oXml.ReadAttribute(sPath, xPath 
				+ "/StepDefinition[@Statement='" + Statement + "']/@ExternalData");
		String sCategory = xPath.replace("/Meta/", "");
		String Instructions = oXml.ReadAttribute(sPath, xPath 
				+ "/StepDefinition[@Statement='" + Statement + "']/@Instructions");
		
		setFrame("Step Definition");
		c = getContentPane(); 
		c.setLayout(null); 
		
		Color TAborderColor = new Color(77, 166, 255);
		Color BtnBorderColor = new Color(255, 102, 0);
		Color RadioBtnBackGround = new Color(255, 255, 255);

		title = fn_AddTextLabel("Edit/Delete Step Definition", "Arial", 20, new Dimension(300, 30), new Point(300, 30));
		statement = fn_AddTextLabel("Statement", "Arial", 15, new Dimension(200, 20), new Point(100,100));
		tname = fn_AddTextField("Arial", 15, new Dimension(270, 20), new Point(200, 100), TAborderColor, Statement);
		ExternalData = fn_AddTextLabel("Data Table?", "Arial", 15, new Dimension(100, 20), new Point(100, 150));

		if (sExternalData.equalsIgnoreCase("yes"))
			yes = fn_AddRadioButton("Yes", "Arial", 15, new Dimension(75, 20), new Point(200, 150), true, RadioBtnBackGround);
		else
			yes = fn_AddRadioButton("Yes", "Arial", 15, new Dimension(75, 20), new Point(200, 150), false, RadioBtnBackGround);

		if (sExternalData.equalsIgnoreCase("no"))
			no = fn_AddRadioButton("No", "Arial", 15, new Dimension(75, 20), new Point(275, 150), true, RadioBtnBackGround);
		else
			no = fn_AddRadioButton("No", "Arial", 15, new Dimension(75, 20), new Point(275, 150), false, RadioBtnBackGround);

		datagp = new ButtonGroup(); 
		datagp.add(yes);
		datagp.add(no);

		category = fn_AddTextLabel("Category", "Arial", 15, new Dimension(100, 20), new Point(100, 200));
		StepType = fn_AddComboBox(categoryList, "Arial", 15, new Dimension(90, 20), new Point(200, 200));
		StepType.setSelectedItem(sCategory);

		fn_AddTextLabel("Parameters", "Arial", 15, new Dimension(100, 20), new Point(100, 250));
		fn_AddTextArea("Arial", 13, new Dimension(270, 40), new Point(200, 250),true, true, TAborderColor);
		
		add = fn_AddTextLabel("Instructions", "Arial", 15, new Dimension(100, 20), new Point(100, 300));
		tadd = fn_AddTextArea("Arial", 13, new Dimension(270, 200), new Point(200, 300),true, true, TAborderColor);
		tadd.setText(Instructions);
		
		update = fn_AddButton("Update", "Arial", 15, new Dimension(100, 20), new Point(300, 525),BtnBorderColor);
		delete = fn_AddButton("Delete", "Arial", 15, new Dimension(100, 20), new Point(450, 525),BtnBorderColor);
		tout = fn_AddTextArea("Arial", 15, new Dimension(300,400), new Point(500,100),true, false, TAborderColor);
		tout.setText(fn_GetFinalResponse());
		res = fn_AddTextLabel("", "Arial", 20, new Dimension(500, 25), new Point(100, 500));
		resadd = fn_AddTextArea("Arial", 13, new Dimension(200, 75), new Point(580, 175),true, true, TAborderColor);

		setVisible(true); 
	} 	
	
	public void setFrame(String sTitle) {
		setTitle(sTitle); 
		setDefaultCloseOperation(HIDE_ON_CLOSE);;
//		getContentPane().setBackground(new Color(255, 255, 230));
	    setUndecorated(true);
	    getRootPane().setWindowDecorationStyle(JRootPane.FRAME);
	    setBounds(300, 90, 900, 600); 
	    try {
	    	setContentPane(new JLabel(new ImageIcon(Toolkit.getDefaultToolkit().getImage(this.getClass().getResource("/resources/background_stepdef.jpg")))));
	    } catch (Exception e) {
	    	System.out.println(e.getMessage());
	    }
		setResizable(false);		
	}

	public JTextArea fn_AddTextArea(String sFont, int fSize, Dimension size, 
			Point iLocation, boolean bLineWrap, boolean bEditable, Color color) {
		
		c = getContentPane(); 
		JTextArea oTextArea = new JTextArea();
		oTextArea.setFont(new Font(sFont, Font.PLAIN, fSize));
		oTextArea.setSize(size); 
		oTextArea.setLocation(iLocation); 
		oTextArea.setLineWrap(bLineWrap); 
		oTextArea.setEditable(bEditable);
		Border border = BorderFactory.createLineBorder(color, 2);
		oTextArea.setBorder(border);		
		JScrollPane scrollPane = new JScrollPane(oTextArea);
		scrollPane.setLocation(iLocation);
		scrollPane.setSize(size);
		scrollPane.setVerticalScrollBarPolicy(ScrollPaneConstants.VERTICAL_SCROLLBAR_ALWAYS);
		
		c.add(scrollPane);
		return oTextArea;
	}
	
	public JTextField fn_AddTextField(String sFont, int fSize, Dimension size, 
			Point iLocation, Color color, String sDefaultText) {
		
		c = getContentPane(); 
		JTextField oTextField = new JTextField();
		oTextField.setFont(new Font(sFont, Font.PLAIN, fSize)); 
		oTextField.setSize(size); 
		oTextField.setLocation(iLocation); 
		Border border = BorderFactory.createLineBorder(color, 2);
		oTextField.setBorder(border);
		oTextField.setText(sDefaultText);
		c.add(oTextField);
		
		return oTextField;
	}
	
	public JLabel fn_AddTextLabel(String sLabel, String sFont, int fSize, Dimension size, 
			Point iLocation) {
		c = getContentPane(); 
		JLabel oTextLabel = new JLabel(sLabel); 
		oTextLabel.setFont(new Font(sFont, Font.BOLD, fSize)); 
		oTextLabel.setSize(size); 
		oTextLabel.setLocation(iLocation); 
		c.add(oTextLabel);
		return oTextLabel;
	}	
	
	public JButton fn_AddButton(String sLabel, String sFont, int fSize, Dimension size, 
			Point iLocation, Color color) {
		
		c = getContentPane(); 
		JButton oButton = new JButton(sLabel); 
		oButton.setFont(new Font(sFont, Font.PLAIN, fSize)); 
		oButton.setSize(size); 
		oButton.setLocation(iLocation); 
		oButton.addActionListener(this);
		Border border = BorderFactory.createLineBorder(color, 2);
		oButton.setBorder(border);		
		c.add(oButton);
		return oButton;
	}		
	
	public JRadioButton fn_AddRadioButton(String sLabel, String sFont, int fSize, Dimension size, 
			Point iLocation, boolean bSelected, Color color) {
		
		c = getContentPane(); 
		JRadioButton oRadioBtn = new JRadioButton(sLabel); 
		oRadioBtn.setFont(new Font(sFont, Font.PLAIN, fSize)); 
		oRadioBtn.setSelected(bSelected); 
		oRadioBtn.setSize(size); 
		oRadioBtn.setLocation(iLocation); 	
		Border border = BorderFactory.createLineBorder(color, 2);
		oRadioBtn.setBorder(border);			
		c.add(oRadioBtn);
		return oRadioBtn;
	}
	
	public JComboBox fn_AddComboBox(String[] sList, String sFont, int fSize, Dimension size, 
			Point iLocation) {
		
		c = getContentPane(); 
		JComboBox oCmbBox = new JComboBox(sList);
		oCmbBox.setFont(new Font(sFont, Font.PLAIN, fSize));
		oCmbBox.setSize(size);
		oCmbBox.setLocation(iLocation);
		c.add(oCmbBox);
		return oCmbBox;
		
	}
	
	public void actionPerformed(ActionEvent e) 
	{ 
		if (e.getSource() == sub) { 
			
			xml oXml = new xml();
			tout.setText(fn_GetFinalResponse());
			
			String xtrnlData;
			if (yes.isSelected()) 
				xtrnlData = "Yes";
			else
				xtrnlData = "No";
			
			oXml.AddToXml(sXMLPath, "/Meta/" + (String)StepType.getSelectedItem(), 
					tname.getText(), xtrnlData, tadd.getText());
			
			res.setText("Step Definition Added/Updated Successfully.."); 
		}	else if (e.getSource() == reset) { 
			String def = ""; 
			tname.setText(def); 
			tadd.setText(def); 
			res.setText(def); 
			tout.setText(def); 
			StepType.setSelectedIndex(0); 
			resadd.setText(def); 
			
		} else if (e.getSource() == update) {
			
			xml oXml = new xml();
			oXml.RemoveFromXml(sXMLPath, sExistingXpath);
			
			tout.setText(fn_GetFinalResponse());
			
			String xtrnlData;
			if (yes.isSelected()) 
				xtrnlData = "Yes";
			else
				xtrnlData = "No";			

			oXml.AddToXml(sXMLPath, "/Meta/" + (String)StepType.getSelectedItem(), 
					tname.getText(), xtrnlData, tadd.getText());
			res.setText("Step Definition Updated Successfully..");
		}else if (e.getSource() == delete) {
			xml oXml = new xml();
			oXml.RemoveFromXml(sXMLPath, sExistingXpath);
			String def = "";
			tname.setText(def); 
			tadd.setText(def);
			res.setText(def);
			tout.setText(def); 
			StepType.setSelectedIndex(0);
			resadd.setText(def);
			res.setText("Step Definition deleted Successfully..");
		}
	} 	
	
	public String fn_GetFinalResponse() {
		String data1; 
		String data 
			= "Name : "
			+ tname.getText() + "\n";
		String xtrnlData;
		if (yes.isSelected()) { 
			data1 = "TestDataNeeded : Yes"
					+ "\n"; 
			xtrnlData = "Yes";
		} else {
			data1 = "TestDataNeeded : No"
					+ "\n"; 
			xtrnlData = "No";
		}
		String data2 = "Category : "+ (String)StepType.getSelectedItem() + "\n";

		String data3 = "Instructions : " + tadd.getText(); 
		return data + data1 + data2 + data3;
	}
} 