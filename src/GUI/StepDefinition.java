package GUI;
//Java program to implement 
//a Simple Registration Form 
//using Java Swing 

import javax.swing.*; 
import java.awt.*; 
import java.awt.event.*; 

class MyFrame 
	extends JFrame 
	implements ActionListener { 

	// Components of the Form 
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

	// constructor, to initialize the components 
	// with default values. 
	public MyFrame(String sPath) 
	{ 
		sXMLPath = sPath;
		setTitle("Step Definition"); 
		setDefaultCloseOperation(HIDE_ON_CLOSE);;
		getContentPane().setBackground(new Color(230, 255, 230));
	    setUndecorated(true);
	    getRootPane().setWindowDecorationStyle(JRootPane.FRAME);
	    setBounds(300, 90, 900, 600); 
		setResizable(false); 

		c = getContentPane(); 
		c.setLayout(null); 

		title = new JLabel("Add Step Definition"); 
		title.setFont(new Font("Arial", Font.PLAIN, 30)); 
		title.setSize(300, 30); 
		title.setLocation(300, 30); 
		c.add(title); 

		statement = new JLabel("Statement"); 
		statement.setFont(new Font("Arial", Font.PLAIN, 15)); 
		statement.setSize(200, 20); 
		statement.setLocation(100, 100); 
		c.add(statement); 

		tname = new JTextField(); 
		tname.setFont(new Font("Arial", Font.PLAIN, 15)); 
		tname.setSize(270, 20); 
		tname.setLocation(200, 100); 
		c.add(tname); 

		ExternalData = new JLabel("External Data?"); 
		ExternalData.setFont(new Font("Arial", Font.PLAIN, 15)); 
		ExternalData.setSize(100, 20); 
		ExternalData.setLocation(100, 150); 
		c.add(ExternalData); 

		yes = new JRadioButton("Yes"); 
		yes.setFont(new Font("Arial", Font.PLAIN, 15)); 
		yes.setSelected(true); 
		yes.setSize(75, 20); 
		yes.setLocation(200, 150); 
		c.add(yes); 

		no = new JRadioButton("No"); 
		no.setFont(new Font("Arial", Font.PLAIN, 15)); 
		no.setSelected(false); 
		no.setSize(80, 20); 
		no.setLocation(275, 150); 
		c.add(no); 

		datagp = new ButtonGroup(); 
		datagp.add(yes);
		datagp.add(no);

		category = new JLabel("Category");
		category.setFont(new Font("Arial", Font.PLAIN, 15)); 
		category.setSize(100, 20);
		category.setLocation(100, 200);
		c.add(category);

		StepType = new JComboBox(categoryList);
		StepType.setFont(new Font("Arial", Font.PLAIN, 15)); 
		StepType.setSize(90, 20);
		StepType.setLocation(200, 200); 
		c.add(StepType); 

		add = new JLabel("Instructions"); 
		add.setFont(new Font("Arial", Font.PLAIN, 15)); 
		add.setSize(100, 20); 
		add.setLocation(100, 250); 
		c.add(add); 

		tadd = new JTextArea(5, 20); 
		tadd.setFont(new Font("Arial", Font.PLAIN, 13)); 
		tadd.setSize(270, 200); 
		tadd.setLineWrap(true);
		tadd.setAutoscrolls(true);
		tadd.setLocation(200, 250); 
		c.add(tadd);

		sub = new JButton("Submit"); 
		sub.setFont(new Font("Arial", Font.PLAIN, 15)); 
		sub.setSize(100, 20); 
		sub.setLocation(150, 475); 
		sub.addActionListener(this); 
		c.add(sub); 

		reset = new JButton("Reset"); 
		reset.setFont(new Font("Arial", Font.PLAIN, 15)); 
		reset.setSize(100, 20); 
		reset.setLocation(270, 475); 
		reset.addActionListener(this); 
		c.add(reset); 

		tout = new JTextArea(); 
		tout.setFont(new Font("Arial", Font.PLAIN, 15)); 
		tout.setSize(300, 400); 
		tout.setLocation(500, 100); 
		tout.setLineWrap(true); 
		tout.setEditable(false); 
		c.add(tout); 

		res = new JLabel(""); 
		res.setFont(new Font("Arial", Font.PLAIN, 20)); 
		res.setSize(500, 25); 
		res.setLocation(100, 500); 
		c.add(res); 

		resadd = new JTextArea(); 
		resadd.setFont(new Font("Arial", Font.PLAIN, 15)); 
		resadd.setSize(200, 75); 
		resadd.setLocation(580, 175); 
		resadd.setLineWrap(true); 
		c.add(resadd); 

		setVisible(true); 
	} 
	
	public MyFrame(String sPath, String Statement, String xPath) 
	{ 
		sXMLPath = sPath;
		sExistingXpath = xPath + "/StepDefinition[@Statement='" + Statement + "']";
		xml oXml = new xml();
		String sExternalData = oXml.ReadAttribute(sPath, xPath + "/StepDefinition[@Statement='" + Statement + "']/@ExternalData");
		String sCategory = xPath.replace("/Meta/", "");
		String Instructions = oXml.ReadAttribute(sPath, xPath + "/StepDefinition[@Statement='" + Statement + "']/@Instructions");
		
		setTitle("Step Definition"); 
		setDefaultCloseOperation(HIDE_ON_CLOSE);
		getContentPane().setBackground(new Color(230, 255, 230));
	    setUndecorated(true);
	    getRootPane().setWindowDecorationStyle(JRootPane.FRAME);
		setBounds(300, 90, 900, 600); 
		setResizable(false); 

		c = getContentPane(); 
		c.setLayout(null); 

		title = new JLabel("Edit/Delete Step Definition"); 
		title.setFont(new Font("Arial", Font.PLAIN, 20)); 
		title.setSize(300, 30); 
		title.setLocation(300, 30); 
		c.add(title); 

		statement = new JLabel("Statement"); 
		statement.setFont(new Font("Arial", Font.PLAIN, 15)); 
		statement.setSize(200, 20); 
		statement.setLocation(100, 100); 
		c.add(statement); 

		tname = new JTextField(); 
		tname.setFont(new Font("Arial", Font.PLAIN, 15)); 
		tname.setSize(270, 20); 
		tname.setLocation(200, 100); 
		tname.setText(Statement);
		c.add(tname); 

		ExternalData = new JLabel("External Data?"); 
		ExternalData.setFont(new Font("Arial", Font.PLAIN, 15)); 
		ExternalData.setSize(100, 20); 
		ExternalData.setLocation(100, 150); 
		c.add(ExternalData); 

		yes = new JRadioButton("Yes"); 
		yes.setFont(new Font("Arial", Font.PLAIN, 15)); 
		yes.setSelected(true); 
		yes.setSize(75, 20); 
		yes.setLocation(200, 150); 
		if (sExternalData.equalsIgnoreCase("yes"))
			yes.setEnabled(true);
		c.add(yes); 

		no = new JRadioButton("No"); 
		no.setFont(new Font("Arial", Font.PLAIN, 15)); 
		no.setSelected(false); 
		no.setSize(80, 20); 
		no.setLocation(275, 150); 
		if (sExternalData.equalsIgnoreCase("no"))
			no.setEnabled(true);
		c.add(no); 

		datagp = new ButtonGroup(); 
		datagp.add(yes);
		datagp.add(no);

		category = new JLabel("Category");
		category.setFont(new Font("Arial", Font.PLAIN, 15)); 
		category.setSize(100, 20);
		category.setLocation(100, 200);
		c.add(category);

		StepType = new JComboBox(categoryList);
		StepType.setFont(new Font("Arial", Font.PLAIN, 15)); 
		StepType.setSize(90, 20);
		StepType.setLocation(200, 200); 
		StepType.setSelectedItem(sCategory);
		c.add(StepType); 

		add = new JLabel("Instructions"); 
		add.setFont(new Font("Arial", Font.PLAIN, 15)); 
		add.setSize(100, 20); 
		add.setLocation(100, 250); 
		c.add(add); 

		tadd = new JTextArea(5, 20); 
		tadd.setFont(new Font("Arial", Font.PLAIN, 13)); 
		tadd.setSize(270, 200); 
		tadd.setLineWrap(true);
		tadd.setAutoscrolls(true);
		tadd.setLocation(200, 250); 
		tadd.setText(Instructions);
		c.add(tadd);

		update = new JButton("Update"); 
		update.setFont(new Font("Arial", Font.PLAIN, 15)); 
		update.setSize(100, 20); 
		update.setLocation(150, 475); 
		update.addActionListener(this); 
		c.add(update); 

		delete = new JButton("Delete"); 
		delete.setFont(new Font("Arial", Font.PLAIN, 15)); 
		delete.setSize(100, 20); 
		delete.setLocation(270, 475); 
		delete.addActionListener(this); 
		c.add(delete); 

		tout = new JTextArea(); 
		tout.setFont(new Font("Arial", Font.PLAIN, 15)); 
		tout.setSize(300, 400); 
		tout.setLocation(500, 100); 
		tout.setLineWrap(true); 
		tout.setEditable(false); 
		c.add(tout); 

		res = new JLabel(""); 
		res.setFont(new Font("Arial", Font.PLAIN, 20)); 
		res.setSize(500, 25); 
		res.setLocation(100, 500); 
		c.add(res); 

		resadd = new JTextArea(); 
		resadd.setFont(new Font("Arial", Font.PLAIN, 15)); 
		resadd.setSize(200, 75); 
		resadd.setLocation(580, 175); 
		resadd.setLineWrap(true); 
		c.add(resadd); 
		
		String data1; 
		String data 
			= "Name : "
			+ Statement + "\n";
		data1 = "TestDataNeeded : " + sExternalData
			+ "\n"; 
		String data2 = "Category : "+ sCategory + "\n";

		String data3 = "Instructions : " + Instructions;
		tout.setText(data + data1 + data2 + data3); 
		tout.setEditable(false); 		

		setVisible(true); 
	} 	

	public void actionPerformed(ActionEvent e) 
	{ 
		if (e.getSource() == sub) { 
			
			xml oXml = new xml();
			
			System.out.println("");
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
			tout.setText(data + data1 + data2 + data3); 
			tout.setEditable(false); 
			oXml.AddToXml(sXMLPath, "/Meta/" + (String)StepType.getSelectedItem(), tname.getText(), xtrnlData, tadd.getText());
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
			System.out.println("");
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
			tout.setText(data + data1 + data2 + data3); 
			tout.setEditable(false); 
			oXml.AddToXml(sXMLPath, "/Meta/" + (String)StepType.getSelectedItem(), tname.getText(), xtrnlData, tadd.getText());
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
} 