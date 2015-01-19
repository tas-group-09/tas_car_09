echo ""
echo "╔═════════════════════════════╗"
echo "║       TAS - Group 09        ║"
echo "╚═════════════════════════════╝"
echo ""
echo "The following actions are available:"


PS3='Please select your corresponding action (4 => Quit): '
options=("Autonomous driving" "Slalom Parcour" "Quit")
select opt in "${options[@]}"
do
    case $opt in
        "Autonomous driving")
            echo "Executing autonomous driving"
	    	roslaunch launch/Round_tas09.launch
            ;;
        "Slalom Parcour")
            echo "Executing slalom Parcour"
        	roslaunch launch/Slalom_tas09.launch
            ;;
        "Quit")
	    echo "Shutting down ..."
            break
            ;;
        *) echo invalid option;;
    esac
done
