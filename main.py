import random as rd
import streamlit as st
import time

def reset_game():
    st.session_state.game_state = "start"
    st.session_state.user_score = 0
    st.session_state.pc_score = 0
    st.session_state.round = 0
    st.session_state.sudden_death = False
    st.session_state.sudden_death_count = 0

def main():
    st.title("Rock Paper Scissors (Best of 3)")
    st.caption("By JKK")
    possibilities = ["Rock", "Paper", "Scissors"]

    # INITIALIZE SESSION STATE
    if "game_state" not in st.session_state:
        st.session_state.game_state = "start"
        st.session_state.user_score = 0
        st.session_state.pc_score = 0
        st.session_state.round = 0
        st.session_state.sudden_death = False
        st.session_state.sudden_death_count = 0

    # LOADING
    if st.session_state.game_state == "start":
        if st.button("PLAY"):
            st.session_state.game_state = "loading"

    if st.session_state.game_state == "loading":
        with st.spinner("Loading"):
            time.sleep(2)

        progress_text = "Getting game ready for you..."
        bar = st.progress(0, text=progress_text)

        for i in range(100):
            time.sleep(0.01)
            bar.progress(i + 1, text=progress_text)

        time.sleep(1)
        bar.empty()
        st.session_state.game_state = "playing"

    # PLAY
    if st.session_state.game_state == "playing":
        st.write(f"Round {st.session_state.round + 1} of 3")
        pc_choice = rd.choice(possibilities)

        col1, col2 = st.columns(2)

        with col1:
            user_choice = st.selectbox("Your choice : ", possibilities, key=f"main_{st.session_state.round}")
        with col2:
            if st.button("Submit Choice", key=f"submit_{st.session_state.round}"):
                # SHOW CHOICES
                st.write(f"👤 You chose : {user_choice}")
                st.write(f"🤖 PC chose : {pc_choice}")

                # DETERMINE WINNER
                if user_choice == pc_choice:
                    st.info("It's a tie")
                elif (user_choice == "Rock" and pc_choice == "Scissors") or \
                        (user_choice == "Paper" and pc_choice == "Rock") or \
                        (user_choice == "Scissors" and pc_choice == "Paper"):
                    st.success("You win this round")
                    st.session_state.user_score += 1
                else:
                    st.warning("PC wins this round")
                    st.session_state.pc_score += 1

                st.session_state.round += 1

                if st.session_state.round >= 3:
                    st.session_state.game_state = "result"
                else:
                    if st.button("Next Round", key=f"next_{st.session_state.round}"):
                        st.session_state.game_state = st.session_state.game_state
                        st.session_state.user_score = st.session_state.user_score
                        st.session_state.pc_score = st.session_state.pc_score
                        st.session_state.round = st.session_state.round

    # RESULTS
    if st.session_state.game_state == "result":
        st.subheader("Final Score")
        st.write(f"Your score : {st.session_state.user_score}")
        st.write(f"PC score : {st.session_state.pc_score}")

        if st.session_state.user_score == st.session_state.pc_score:
            st.error("You have reached SUDDEN DEATH!")
            st.session_state.sudden_death = True
            st.session_state.game_state = "sudden_death"
        elif st.session_state.user_score > st.session_state.pc_score:
            st.balloons()
            st.success("🎉 You win the game")
            if st.button("PLAY AGAIN"):
                reset_game()
        else:
            st.error("💻 PC wins the game")
            if st.button("PLAY AGAIN"):
                reset_game()


    # SUDDEN DEATH
    if st.session_state.game_state == "sudden_death":
        st.subheader("SUDDEN DEATH")
        pc_choice = rd.choice(possibilities)

        col1, col2 = st.columns(2)

        with col1:
            user_choice = st.selectbox("Your choice : ", possibilities, key=f"sudden_death_main_{st.session_state.sudden_death_count}")
        with col2:
            # SHOW CHOICES
            if st.button("Submit Choice", key=f"sudden_death_submit_{st.session_state.sudden_death_count}"):
                st.write(f"👤 You chose : {user_choice}")
                st.write(f"🤖 PC chose : {pc_choice}")

                # STAY IN SUDDEN DEATH
                if user_choice == pc_choice:
                    st.warning("ANOTHER TIE!")
                    st.session_state.sudden_death_count += 1

                    if st.button("Next Round", key=f"sudden_death_next_{st.session_state.sudden_death_count}"):
                        st.session_state.game_state = "sudden_death"
                # DETERMINE WINNER
                elif (user_choice == "Rock" and pc_choice == "Scissors") or \
                        (user_choice == "Paper" and pc_choice == "Rock") or \
                        (user_choice == "Scissors" and pc_choice == "Paper"):
                    st.success("You win this round")
                    st.session_state.user_score += 1
                    st.session_state.game_state = "sudden_death_result"
                else:
                    st.error("PC wins this round")
                    st.session_state.pc_score += 1
                    st.session_state.game_state = "sudden_death_result"

     # SUDDEN DEATH RESULTS
    if st.session_state.game_state == "sudden_death_result":
        st.subheader("Final Score")
        st.write(f"Your score : {st.session_state.user_score}")
        st.write(f"PC score : {st.session_state.pc_score}")

        if st.session_state.user_score > st.session_state.pc_score:
            st.balloons()
            st.success("🎉 You win the game")
        else:
            st.error("💻 PC wins the game")

        if st.button("PLAY AGAIN"):
            reset_game()

if __name__ == "__main__":
    main()