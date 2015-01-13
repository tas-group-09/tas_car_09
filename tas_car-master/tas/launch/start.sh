echo ""
echo "╔═════════════════════════════╗"
echo "║       TAS - Group 09        ║"
echo "╚═════════════════════════════╝"
echo ""
echo "The following actions are available:"


PS3='Please select your corresponding action (4 => Quit): '
options=("Autonomous driving (RVIZ)" "Slalom Parcour" "Empty" "Quit")
select opt in "${options[@]}"
do
    case $opt in
        "Autonomous driving (RVIZ)")
            echo "Executing autonomous driving (RVIZ)"
	    roslaunch run_rviz.launch
            ;;
        "Slalom Parcour")
            echo "Executing slalom parcour (not implemented so far)"
            ;;
        "Empty")
            echo "Nothing to do here..."
            ;;
        "Quit")
	    echo "Shutting down ..."
            break
            ;;
        *) echo invalid option;;
    esac
done
