echo ""
echo "╔═════════════════════════════╗"
echo "║       TAS - Group 09        ║"
echo "╚═════════════════════════════╝"
echo ""
echo "The following actions are available:"


PS3='Please select your corresponding action: '
options=("Autonomous driving (RVIZ)" "Slalom Parcour" "Option 3" "Quit")
select opt in "${options[@]}"
do
    case $opt in
        "Autonomous driving (RVIZ)")
            echo "Executing autonomous driving (RVIZ)"
	    roslaunch run_rviz.launch
            ;;
        "Slalom Parcour")
            echo "Executing slalom Parcour"
            ;;
        "Option 3")
            echo "you chose choice 3"
            ;;
        "Quit")
	    echo "Shutting down ..."
            break
            ;;
        *) echo invalid option;;
    esac
done
