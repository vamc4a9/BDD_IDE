package GUI;

import java.awt.Color;
import java.awt.Dimension;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.FocusEvent;
import java.awt.event.FocusListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.Vector;
import javax.swing.AbstractAction;
import javax.swing.JButton;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JMenuItem;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JPopupMenu;
import javax.swing.JRootPane;
import javax.swing.JScrollPane;
import javax.swing.JSplitPane;
import javax.swing.JTabbedPane;
import javax.swing.JTextArea;
import javax.swing.JTree;
import javax.swing.SwingUtilities;
import javax.swing.UIManager;
import javax.swing.event.TreeSelectionEvent;
import javax.swing.event.TreeSelectionListener;
import javax.swing.plaf.ColorUIResource;
import javax.swing.plaf.metal.DefaultMetalTheme;
import javax.swing.plaf.metal.MetalLookAndFeel;
import javax.swing.tree.DefaultMutableTreeNode;
import javax.swing.tree.DefaultTreeModel;
import javax.swing.tree.TreePath;
import javax.swing.tree.TreeSelectionModel;

import org.apache.commons.io.FileUtils;
import org.dom4j.Document;
import org.dom4j.DocumentException;
import org.dom4j.Element;
import org.dom4j.io.SAXReader;
 
public class Driver extends JPanel
                      implements TreeSelectionListener, ActionListener, MouseListener, FocusListener {
	private static final long serialVersionUID = 1L;
	static private final String newline = "\n";
	private JTabbedPane editor;
	JMenuItem oSave, oClose, oCloseAll;
    JButton btnOpen, addNewStepDef, btnMeta, Refresh, RefreshProject, EditStepDef, btnSave, btnSaveAll;
    public JTree stepDef;
    public JTree project;
    private Map<Integer, String> sTabsList = new HashMap<Integer, String>();
    private Map<Integer, String> sOriginalText = new HashMap<Integer, String>();
    private Map<Integer, TreePath[]> sSelectedPath = new HashMap<Integer, TreePath[]>();
    private List<String> sOpenedTabs = new ArrayList<String>();
    Integer tabIndex;
    
    private static String sCurrentProject, sCurrentMetaFile;
    JSplitPane ProjectExplorerPane, StepDefExplorerPane;
    private static boolean useSystemLookAndFeel = false;
    public static JFrame fParent;
 
    public Driver(String sData) {
        super(new GridLayout(1,0));
        fParent.addWindowListener(new WListener());
        DefaultMutableTreeNode top = null;
        JScrollPane treeView = new JScrollPane();
        treeView.addMouseListener(this);
        JScrollPane stepDefTree = new JScrollPane();
        
        project = new JTree(top);
        project.setName("ProjectExplorer");
        stepDef = new JTree(top);
        stepDef.setName("StepDefinition");
        
        project.addTreeSelectionListener(this);
        project.addMouseListener(this);
        
        stepDef.getSelectionModel().setSelectionMode
                (TreeSelectionModel.SINGLE_TREE_SELECTION);
 
        JScrollPane stepView = new JScrollPane(stepDef);        
 
        editor = new JTabbedPane();
        JScrollPane jEditor = new JScrollPane(editor);
        editor.setBackground(new Color(230, 255, 230)); 
        
        //Creating the project explorer pane
        JPanel PrjectOpen = new JPanel();
        btnOpen = new JButton("Open");
        btnOpen.addActionListener(this);
        btnSave = new JButton("Save");
        btnSave.setEnabled(false);
        btnSave.addActionListener(this);
        
        btnSaveAll = new JButton("SaveAll");
        btnSaveAll.setEnabled(false);
        btnSaveAll.addActionListener(this);
        
        RefreshProject = new JButton("Refresh");
        RefreshProject.setEnabled(false);
//        RefreshProject.setEnabled(false);
        PrjectOpen.add(btnOpen);
        PrjectOpen.add(btnSave);
        PrjectOpen.add(btnSaveAll);
        PrjectOpen.add(RefreshProject);		
        RefreshProject.addActionListener(this);
        ProjectExplorerPane = new JSplitPane(JSplitPane.VERTICAL_SPLIT);
        ProjectExplorerPane.setTopComponent(PrjectOpen);
        ProjectExplorerPane.setDividerLocation(0.5);
        ProjectExplorerPane.setBottomComponent(treeView);
        ProjectExplorerPane.setBackground(new Color(230, 255, 230));
        
        //Creating the step definition explorer pane
        JPanel StepDefOpen = new JPanel();
        btnMeta = new JButton("Load");
        btnMeta.addActionListener(this);
        
        addNewStepDef = new JButton("Add");
        addNewStepDef.addActionListener(this);
        addNewStepDef.setEnabled(false);
        
		EditStepDef = new JButton("View/Edit");
		EditStepDef.setEnabled(false);
		EditStepDef.addActionListener(this);
		
		Refresh = new JButton("Refresh");
		Refresh.addActionListener(this);
		Refresh.setEnabled(false);
		
		StepDefOpen.add(btnMeta);
		StepDefOpen.add(addNewStepDef);
		StepDefOpen.add(EditStepDef);
		StepDefOpen.add(Refresh);
        StepDefExplorerPane = new JSplitPane(JSplitPane.VERTICAL_SPLIT);
        
        StepDefExplorerPane.setTopComponent(StepDefOpen);
        StepDefExplorerPane.setBottomComponent(stepDefTree);
        
        //Creating the step definition explorer pane
        JSplitPane ExplorerPane = new JSplitPane(JSplitPane.VERTICAL_SPLIT);
        setDividerLocation(ExplorerPane, 0.5);
        ExplorerPane.setTopComponent(ProjectExplorerPane);
        ExplorerPane.setBottomComponent(StepDefExplorerPane);
        
        JSplitPane splitPane = new JSplitPane(JSplitPane.HORIZONTAL_SPLIT);
        setDividerLocation(splitPane, 0.32);
        splitPane.setTopComponent(ExplorerPane);
        splitPane.setBottomComponent(jEditor);
 
        Dimension minimumSize = new Dimension(100, 50);
        jEditor.setMinimumSize(minimumSize);
        treeView.setMinimumSize(minimumSize);
        stepView.setMinimumSize(minimumSize);
        stepDefTree.setMinimumSize(minimumSize);
        splitPane.setDividerLocation(100); 
        splitPane.setPreferredSize(new Dimension(500, 300));
 
        add(splitPane);

        editor.addMouseListener(new MouseAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) 
            {
                if(SwingUtilities.isRightMouseButton(e))
                {
                    JPopupMenu menu = new JPopupMenu();
                    
                    JMenuItem closer = new JMenuItem(new AbstractAction("Close") {
                        @Override
                        public void actionPerformed(ActionEvent e) {
                        	boolean sFlag = true;
                        	if (editor.getTitleAt(editor.getSelectedIndex()).startsWith("*")) {
                        		
                        		Object[] options1 = {"Save",
                                        "Don't Save", 
                                        "Cancel"};

                        		int j = JOptionPane.showOptionDialog(null,
                                        "Save '"+editor.getTitleAt(editor.getSelectedIndex()).replace("*", "") + ".feature"+"'?",
                                        "Save Resource!",
                                        JOptionPane.YES_NO_CANCEL_OPTION,
                                        JOptionPane.PLAIN_MESSAGE,
                                        null,
                                        options1,
                                        null);
                       
						        if (j == 0) {
						        	sFlag = true;
						        	fn_SaveCurrentTab();
						        } else if (j == 1) {
						        	sFlag = true;
						        } else {
						        	sFlag = false;
						        }
                        	}
                        	
                        	if (sFlag) {
                            	sOpenedTabs.remove(editor.getTitleAt(editor.getSelectedIndex()).replace("*", "") + ".feature");
                            	TreePath[] nodeToRemove = sSelectedPath.get(editor.getSelectedIndex() + 1);
                            	int iSelectedIndex = editor.getSelectedIndex();
                            	editor.removeTabAt(editor.getSelectedIndex());
                            	removeCurrentNode(project, nodeToRemove);
                            	
            		            Set<Integer> sKeys = sTabsList.keySet();
            		            boolean bFlag = false;
            		            int iTotalKeys = sKeys.size();
            		            for(int key = 1; key<=iTotalKeys; key++) {
    								if (key == iSelectedIndex + 1) {
    									sTabsList.remove(key);
    									sSelectedPath.remove(key);
    									sOriginalText.remove(key);
    									bFlag = true;
    								} else if (bFlag) {
    									sTabsList.put(key-1, sTabsList.get(key));
    									sOriginalText.put(key-1, sTabsList.get(key));
    									sSelectedPath.put(key-1, sSelectedPath.get(key));
    								}
            		            }
            		            
            		            if (iTotalKeys > 1) {
            		            	sTabsList.remove(iTotalKeys);
            		            	sOriginalText.remove(iTotalKeys);
            		            	sSelectedPath.remove(iTotalKeys);
            		            }
            		            
            		            tabIndex--;                        		
                        	}
                        }
                    });
                    
                    JMenuItem save = new JMenuItem(new AbstractAction("Save") {
                        @Override
                        public void actionPerformed(ActionEvent e) {
                        	fn_SaveCurrentTab();
                        }
                    });
                    
                    menu.add(save);
                    menu.add(closer);
                    menu.show(editor, e.getX(), e.getY());
                }
            }
        });        
        
    }
    
    static void setDividerLocation(
    	    final JSplitPane splitPane, final double location)
    	{
    	    SwingUtilities.invokeLater(new Runnable()
    	    {
    	        @Override
    	        public void run()
    	        {
    	            splitPane.setDividerLocation(location);
    	            splitPane.validate();
    	        }
    	    });
    	}
    
    public void valueChanged(TreeSelectionEvent e) {
    	if (e.getSource() == stepDef) {
            DefaultMutableTreeNode node = (DefaultMutableTreeNode)
            		((JTree) e.getSource()).getLastSelectedPathComponent();
            try {
	            if (node.getChildCount() == 0) {
	            	EditStepDef.setEnabled(true);
	            } else {
	            	EditStepDef.setEnabled(false);
	            }
            } catch (Exception e3) {
            	EditStepDef.setEnabled(false);
            	System.out.println(e3.getMessage());
            }
	            
    	}
    }
    
    public void fn_SaveCurrentTab() {
        JTextArea oEditor = (JTextArea) editor.getSelectedComponent();
        String sFile = sTabsList.get(editor.getSelectedIndex() + 1);
        try {
            FileWriter myWriter = new FileWriter(sFile);
            myWriter.write(oEditor.getText());
            myWriter.close();
          } catch (Exception e2) {
            e2.printStackTrace();
          }        		            
        sOriginalText.put(editor.getSelectedIndex(), oEditor.getText());
        editor.setTitleAt(editor.getSelectedIndex(), editor.getTitleAt(editor.getSelectedIndex()).replace("*", ""));    	
    }
    
    public int findTabByName(String title)  
    {
		int tabCount = editor.getTabCount();
		for (int i=0; i < tabCount; i++) {
			String tabTitle = editor.getTitleAt(i);
			if (tabTitle.equals(title)) return i;
		}
		return -1;
	}
 
    private DefaultMutableTreeNode ReadFeature(String sFile) {
        DefaultMutableTreeNode top = null;
        try {
	    	File file=new File(sFile);
	    	FileReader fr=new FileReader(file);
	    	BufferedReader br=new BufferedReader(fr);
	    	String line;  
	    	while((line=br.readLine())!=null)
	    	{  
	    		if (line.startsWith("Feature:")) {
	    			top = new DefaultMutableTreeNode(line);
	    			break;
	    		}
	    	}   
        } catch (Exception e) {
        	e.printStackTrace();
        }
    	ReadScenarios(sFile, top);
        return top;
    }
    
    private DefaultMutableTreeNode ReadScenarios(String sFile, DefaultMutableTreeNode top1) {
    	try  {
	    	File file=new File(sFile);
	    	FileReader fr=new FileReader(file);
	    	BufferedReader br=new BufferedReader(fr);
	    	JTextArea sNewTab = new JTextArea();
	    	sNewTab.addFocusListener(this);
	    	sNewTab.setEditable(true);
	    	String line;  
	    	while((line=br.readLine())!=null)  
	    	{  
	    		sNewTab.append(line);
	    		sNewTab.append(newline);
	    		if (line.trim().startsWith("Scenario:") || line.trim().startsWith("Scenario Outline:")) {
	    			top1.add(new DefaultMutableTreeNode(line));
	    		}
	    	}  
	    	fr.close();
	    	editor.addTab(sFile.split("\\\\")[sFile.split("\\\\").length-1].replace(".feature", ""), sNewTab);
	    	sOpenedTabs.add(sFile.split("\\\\")[sFile.split("\\\\").length-1]);
	    	sOriginalText.put(tabIndex, sNewTab.getText());
	    	sTabsList.put(tabIndex, sFile);
//	    	bSaveFlags.put(tabIndex, true);
	    	sSelectedPath.put(tabIndex, project.getSelectionPaths());
	    	editor.setFocusable(true);
	    	editor.setSelectedIndex(tabIndex-1);
	    	tabIndex++;
	    	return top1;
    	} catch(IOException e)  {
    		e.printStackTrace();
    		return null;
    	}  
    }
    
    /** Add nodes from under "dir" into curTop. Highly recursive. */
    public DefaultMutableTreeNode addNodes(DefaultMutableTreeNode curTop, File dir, boolean parent) {
      String curPath = dir.getPath();
      DefaultMutableTreeNode curDir = null;
      if (parent) {
    	  curDir = new DefaultMutableTreeNode(dir.getPath());
      } else {
    	  curDir = new DefaultMutableTreeNode(dir.getPath().split("\\\\")[dir.getPath().split("\\\\").length-1]);
      }
      if (curTop != null) { // should only be null at root
        curTop.add(curDir);
      }
      Vector ol = new Vector();
      String[] tmp = dir.list();
      for (int i = 0; i < tmp.length; i++)
        ol.addElement(tmp[i]);
      Collections.sort(ol, String.CASE_INSENSITIVE_ORDER);
      File f;
      Vector files = new Vector();
      // Make two passes, one for Dirs and one for Files. This is #1.
      for (int i = 0; i < ol.size(); i++) {
        String thisObject = (String) ol.elementAt(i);
        String newPath;
        if (curPath.equals("."))
          newPath = thisObject;
        else
          newPath = curPath + File.separator + thisObject;
        if ((f = new File(newPath)).isDirectory())
          addNodes(curDir, f, false);
        else
          files.addElement(thisObject);
      }
      // Pass two: for files.
      for (int fnum = 0; fnum < files.size(); fnum++)
        curDir.add(new DefaultMutableTreeNode(files.elementAt(fnum)));
      return curDir;
    }

    private static void createAndShowGUI() {
    	
//    	MetalLookAndFeel.setCurrentTheme(new MyDefaultMetalTheme());
    	
        if (useSystemLookAndFeel) {
            try {
//            	UIManager.setLookAndFeel(new MetalLookAndFeel());
                UIManager.setLookAndFeel(
                    UIManager.getSystemLookAndFeelClassName());
            } catch (Exception e) {
                System.err.println("Couldn't use system look and feel.");
            }
        }
        
 
        fParent = new JFrame("BDD Editor");
        fParent.setDefaultCloseOperation(JFrame.DO_NOTHING_ON_CLOSE);
        fParent.setUndecorated(true);
        fParent.getRootPane().setWindowDecorationStyle(JRootPane.FRAME);  
        fParent.getContentPane().setBackground(new Color(230, 255, 230));
        fParent.add(new Driver(""));
        fParent.setSize(1000, 600);
        fParent.setLocation(300, 50); 
        fParent.setVisible(true);
        
    }
        
	public void actionPerformed(ActionEvent e) {

        if (e.getSource() == btnOpen) {
        	if (sOpenedTabs.size() > 0) {
        		msgbox("Close all the opened tabs before loadig a new project");
        	} else {
        		sTabsList.clear();
        		sSelectedPath.clear();
        		sOpenedTabs.clear();
        		sOriginalText.clear();
        		
	        	tabIndex = 1;
	        	JFileChooser fc=new JFileChooser();    
	        	fc.setDialogTitle("LoadProject");
	        	fc.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);
	            int returnVal=fc.showOpenDialog(this);
	            if (returnVal == JFileChooser.APPROVE_OPTION) {
	                File file = fc.getSelectedFile();
	                DefaultMutableTreeNode top = addNodes(null, file, true);
	                project = new JTree(top);
	                project.setName("ProjectExplorer");
	                JScrollPane treeView = new JScrollPane(project);
	                project.addTreeSelectionListener(this);
	                project.addMouseListener(this);
	                ProjectExplorerPane.setBottomComponent(treeView);
	                sCurrentProject = file.getAbsolutePath();
	                RefreshProject.setEnabled(true);
	            }
        	}
        } else if (e.getSource() == btnMeta) {
        	JFileChooser fc=new JFileChooser();    
        	fc.setDialogTitle("LoadMeta");
            int returnVal=fc.showOpenDialog(this);
            if (returnVal == JFileChooser.APPROVE_OPTION) {
                File file = fc.getSelectedFile();
            	stepDef = build(file.getAbsolutePath());
            	stepDef.setName("StepDefinition");
            	JScrollPane treeView = new JScrollPane(stepDef);
            	stepDef.addTreeSelectionListener(this);
            	stepDef.addMouseListener(this);
            	StepDefExplorerPane.setBottomComponent(treeView);
                sCurrentMetaFile = file.getAbsolutePath();
                addNewStepDef.setEnabled(true);
                Refresh.setEnabled(true);
            }
        } else if (e.getSource() == Refresh) {
        	stepDef = build(sCurrentMetaFile);
        	stepDef.setName("StepDefinition");
        	JScrollPane treeView = new JScrollPane(stepDef);
        	stepDef.addTreeSelectionListener(this);
        	stepDef.addMouseListener(this);        	
        	StepDefExplorerPane.setBottomComponent(treeView);
        } else if (e.getSource() == RefreshProject){
            DefaultMutableTreeNode top = addNodes(null, new File(sCurrentProject), true);
            project = new JTree(top);
            project.setName("ProjectExplorer");
            JScrollPane treeView = new JScrollPane(project);
            project.addTreeSelectionListener(this);
            project.addMouseListener(this);
            ProjectExplorerPane.setBottomComponent(treeView);
        } else if (e.getSource() == addNewStepDef) {
        	MyFrame f = new MyFrame(sCurrentMetaFile); 
        } else if (e.getSource() == btnSave) {
            JTextArea oEditor = (JTextArea) editor.getSelectedComponent();
            String sFile = sTabsList.get(editor.getSelectedIndex() + 1);
			try {
				FileWriter myWriter = new FileWriter(sFile);
				myWriter.write(oEditor.getText());
				myWriter.close();
			} catch (Exception e2) {
				e2.printStackTrace();
			}
            sOriginalText.put(editor.getSelectedIndex(), oEditor.getText());
            editor.setTitleAt(editor.getSelectedIndex(), editor.getTitleAt(editor.getSelectedIndex()).replace("*", ""));
        } else if (e.getSource() == btnSaveAll) {
            int tabCount = editor.getTabCount();
            for (int i=0; i < tabCount; i++) 
            {
            	JTextArea oEditor = (JTextArea) editor.getComponent(i);
                String sFile = sTabsList.get(i + 1);
    			try {
    				FileWriter myWriter = new FileWriter(sFile);
    				myWriter.write(oEditor.getText());
    				myWriter.close();
    			} catch (Exception e2) {
    				e2.printStackTrace();
    			}
                sOriginalText.put(i+1, oEditor.getText());
                editor.setTitleAt(i, editor.getTitleAt(i).replace("*", ""));
            }
        } else if (e.getSource() == EditStepDef) {
            DefaultMutableTreeNode node = (DefaultMutableTreeNode)
            		stepDef.getLastSelectedPathComponent();
            
            String sFullPath = "";
            if (node == null) return;
            for (int i = 0; i<node.getPath().length-1;i++) {
            	if (i == 0)
            		sFullPath = node.getPath()[i].toString();
            	else
            		sFullPath = sFullPath + "/" + node.getPath()[i];
            }
            
            MyFrame f = new MyFrame(sCurrentMetaFile, node.toString(), "/"+sFullPath);
        }
	}
	
	public JTree build(String pathToXml) {
		SAXReader reader = new SAXReader();
		Document doc;
		try {
			doc = reader.read(pathToXml);
			return new JTree(build(doc.getRootElement(), false));
		} catch (DocumentException e) {
			e.printStackTrace();
			return null;
		}
	}

	public DefaultMutableTreeNode build(Element e, boolean bStep) {
		DefaultMutableTreeNode result = null;
		if (bStep)
			result = new DefaultMutableTreeNode(e.attribute("Statement").getValue());
		else
			result = new DefaultMutableTreeNode(e.getName());
	   
	   for(Object o : e.elements()) {
	      Element child = (Element) o;
	      if (child.getName().equalsIgnoreCase("stepdefinition"))
	    	  result.add(build(child, true));
	      else
	    	  result.add(build(child, false));
	   }
	   return result;         
	}
	
	public void msgbox(String title) {
		
        JFrame oFrame = new JFrame("Message!");
        oFrame.setDefaultCloseOperation(JFrame.HIDE_ON_CLOSE);
        
        JOptionPane.showMessageDialog(oFrame,
        		title,
        	    "Message",
        	    JOptionPane.INFORMATION_MESSAGE);
        
	}	
	
    public static void main(String[] args) {
        javax.swing.SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                createAndShowGUI();
            }
        });
    }

	@Override
	public void mouseClicked(MouseEvent e) {
		JTree tree = (JTree) e.getSource();
		if (tree.getName()=="StepDefinition") {
			if (e.getClickCount() == 2) {
	            DefaultMutableTreeNode node = (DefaultMutableTreeNode)
	            		tree.getLastSelectedPathComponent();
	            if (node.getChildCount() == 0) {
	            	if (editor.getSelectedIndex() >= 0) {
			            JTextArea oEditor = (JTextArea) editor.getSelectedComponent();
			            oEditor.insert(node.toString(), oEditor.getCaretPosition());
			            oEditor.insert(newline, oEditor.getCaretPosition());
	            	}
	            }
			}
		} else if (tree.getName()=="ProjectExplorer") {
			if (e.getButton() == 3) {
			    int x = e.getX();
			    int y = e.getY();
			    TreePath path = tree.getPathForLocation(x, y);
			    if (path == null)
			      return;
			    
			    DefaultMutableTreeNode rightClickedNode = (DefaultMutableTreeNode) path
			        .getLastPathComponent();

			    TreePath[] selectionPaths = tree.getSelectionPaths();

			    boolean isSelected = false;
			    if (selectionPaths != null) {
			      for (TreePath selectionPath : selectionPaths) {
			        if (selectionPath.equals(path)) {
			          isSelected = true;
			        }
			      }
			    }
			    if (!isSelected) {
			      tree.setSelectionPath(path);
			    }
			    
		        String sFullPath = "";
		        
		        if (rightClickedNode == null) return;
		        for (int i = 0; i<rightClickedNode.getPath().length;i++) {
		        	if (i == 0) {
		        		sFullPath = rightClickedNode.getPath()[i].toString();
		        	} else {
		        		sFullPath = sFullPath + "\\" + rightClickedNode.getPath()[i];
		        	}
		        }
		        
			    if (rightClickedNode.toString().endsWith(".feature")) {
					JPopupMenu popup = new JPopupMenu();
					final JMenuItem DeleteFile = new JMenuItem("Delete");
					
					DeleteFile.addActionListener(new ActionListener() {
					    public void actionPerformed(ActionEvent ev) {
					    	if (sOpenedTabs.contains(rightClickedNode.toString())) {
						        JFrame frm=new JFrame();   
						        JOptionPane.showMessageDialog(frm, rightClickedNode.toString() + " is already opened, please save the changes and close the tab before deleting!");
					    	} else {
						        JFrame frm=new JFrame();   
						        int j = JOptionPane.showConfirmDialog(frm, "Are you sure?");

						        String sFullPath = "";
						        for (int i = 0; i<rightClickedNode.getPath().length;i++) {
						        	if (i == 0) {
						        		sFullPath = rightClickedNode.getPath()[i].toString();
						        	} else {
						        		sFullPath = sFullPath + "\\" + rightClickedNode.getPath()[i];
						        	}
						        }			        
						        if (j==0) {
						            try {
						                File file = new File(sFullPath);
						                FileUtils.forceDelete(file);
						             } catch(Exception e) {
						                e.printStackTrace();
						             }
						        }
						        
						        RemoveNode(tree, rightClickedNode);					    		
					    	}
					    }
					});
					
					popup.add(DeleteFile);
					popup.show(tree, x, y);
			    } else if (!sFullPath.contains(".feature") && (rightClickedNode.getChildCount() !=0)) {
					JPopupMenu popup = new JPopupMenu();
					final JMenuItem newFeatureFile = new JMenuItem("NewFeatureFile");
					final JMenuItem DeleteFile = new JMenuItem("Delete");
					final JMenuItem Refresh = new JMenuItem("Refresh");
					newFeatureFile.addActionListener(new ActionListener() {
					    public void actionPerformed(ActionEvent ev) {
					        JFrame frm=new JFrame();   
					        String name=JOptionPane.showInputDialog(frm,"Enter new feature file name \n example: test.feature");
					        String sFullPath = "";
					        for (int i = 0; i<rightClickedNode.getPath().length;i++) {
					        	if (i == 0) {
					        		sFullPath = rightClickedNode.getPath()[i].toString();
					        	} else {
					        		sFullPath = sFullPath + "\\" + rightClickedNode.getPath()[i];
					        	}
					        }			        
					        if (!name.contentEquals("")) {
					            try {
					                File file = new File(sFullPath + "\\" + name);
					                file.createNewFile();
					             } catch(Exception e) {
					                e.printStackTrace();
					             }
					        }
					        updateTree(name, tree, rightClickedNode);
					    }
					});
					
//					Refresh.addActionListener(new ActionListener() {
//					    public void actionPerformed(ActionEvent ev) {
//					    	tree.scrollPathToVisible(new TreePath(rightClickedNode.getPath()));
//				            DefaultTreeModel model = (DefaultTreeModel) project.getModel();
//				            model.reload(rightClickedNode);					        
//					    }
//					});
					
					popup.add(newFeatureFile);
//					popup.add(Refresh);
					popup.show(tree, x, y);
			    } else {

			    }
			} else if (e.getClickCount() == 2) {
	            DefaultMutableTreeNode node = (DefaultMutableTreeNode)
	            		tree.getLastSelectedPathComponent();
	            
	            String sFullPath = "";
	            if (node == null) return;
	            for (int i = 0; i<node.getPath().length;i++) {
	            	if (i == 0) {
	            		sFullPath = node.getPath()[i].toString();
	            	} else {
	            		sFullPath = sFullPath + "\\" + node.getPath()[i];
	            	}
	            }
	            DefaultMutableTreeNode top = null;
	            
	            if (node.toString().toLowerCase().endsWith(".feature")) {
	            	if (!sOpenedTabs.contains(node.toString())) {
	            		node.removeAllChildren();
		            	top = ReadFeature(sFullPath);
		            	try {
		            		node.add(top);
		            	} catch (Exception e3) {
		            		node.add(new DefaultMutableTreeNode("There are no scenarios"));
		            	}
	            	} else {
	            		editor.setSelectedIndex(findTabByName(node.toString().replace(".feature","")));
	            	}
	            	btnSave.setEnabled(true);
	            	btnSaveAll.setEnabled(true);
	            }
	            tree.scrollPathToVisible(new TreePath(node.getPath()));
	            DefaultTreeModel model = (DefaultTreeModel) tree.getModel();
	            model.reload(node);
			}			
		}
	}
	
	public void RemoveNode(JTree tree, DefaultMutableTreeNode node) {
		DefaultTreeModel model = (DefaultTreeModel) tree.getModel();
        if (node.getParent() != null) {
            model.removeNodeFromParent(node);
        }
	}
	
    public void removeCurrentNode(JTree tree, TreePath[] paths) {
    	
    	DefaultMutableTreeNode aNode = (DefaultMutableTreeNode) (paths[0].getLastPathComponent());
        for(int i = 0 ; i < aNode.getChildCount() ; i++)
        {
        	RemoveNode(tree, (DefaultMutableTreeNode)aNode.getChildAt(i));
        }
        
    }	
    
	public void updateTree(final String nodeToAdd, JTree tree, DefaultMutableTreeNode parent) {
		DefaultTreeModel model = (DefaultTreeModel) tree.getModel();
		DefaultMutableTreeNode child = new DefaultMutableTreeNode(nodeToAdd);
		model.insertNodeInto(child, parent, parent.getChildCount());
		tree.scrollPathToVisible(new TreePath(child.getPath()));
		model.reload(child);
	}
	
	@Override
	public void mouseEntered(MouseEvent e) {
		
	}
	@Override
	public void mouseExited(MouseEvent e) {
		
	}
	@Override
	public void mousePressed(MouseEvent e) {
		
	}
	@Override
	public void mouseReleased(MouseEvent e) {
		
	}

	@Override
	public void focusGained(FocusEvent e) {
        JTextArea oEditor = (JTextArea) editor.getSelectedComponent();
        String sText = sOriginalText.get(editor.getSelectedIndex() + 1);
        if (!sText.equals(oEditor.getText())) {
        	if (!editor.getTitleAt(editor.getSelectedIndex()).startsWith("*"))
        		editor.setTitleAt(editor.getSelectedIndex(), "*" + editor.getTitleAt(editor.getSelectedIndex()));
        }
	}

	@Override
	public void focusLost(FocusEvent arg0) {
        JTextArea oEditor = (JTextArea) editor.getSelectedComponent();
        String sText = sOriginalText.get(editor.getSelectedIndex() + 1);
        if (!sText.equals(oEditor.getText())) {
        	if (!editor.getTitleAt(editor.getSelectedIndex()).startsWith("*"))
        		editor.setTitleAt(editor.getSelectedIndex(), "*" + editor.getTitleAt(editor.getSelectedIndex()));
        }
	}
}

class WListener extends WindowAdapter {
	public void windowClosing(WindowEvent e) {
        String ObjButtons[] = {"Yes","No"};
        int PromptResult = JOptionPane.showOptionDialog(null,"Exit the BDD Editor? Any unsaved changes will be lost!","Confirm Exit",JOptionPane.DEFAULT_OPTION,JOptionPane.WARNING_MESSAGE,null,ObjButtons,ObjButtons[1]);
        if(PromptResult==JOptionPane.YES_OPTION)
        {
            System.exit(0);
        }
	}
}

class MyDefaultMetalTheme extends DefaultMetalTheme {
	  public ColorUIResource getWindowTitleInactiveBackground() {
	    return new ColorUIResource(java.awt.Color.orange);
	  }

	  public ColorUIResource getWindowTitleBackground() {
	    return new ColorUIResource(java.awt.Color.orange);
	  }

	  public ColorUIResource getPrimaryControlHighlight() {
	    return new ColorUIResource(java.awt.Color.orange);
	  }

	  public ColorUIResource getPrimaryControlDarkShadow() {
	    return new ColorUIResource(java.awt.Color.orange);
	  }

	  public ColorUIResource getPrimaryControl() {
	    return new ColorUIResource(java.awt.Color.orange);
	  }

	  public ColorUIResource getControlHighlight() {
	    return new ColorUIResource(java.awt.Color.orange);
	  }

	  public ColorUIResource getControlDarkShadow() {
	    return new ColorUIResource(java.awt.Color.orange);
	  }

	  public ColorUIResource getControl() {
	    return new ColorUIResource(java.awt.Color.orange);
	  }
	}