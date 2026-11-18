
import streamlit as st

st.title("♠️ Blackjack Game")
st.write("Welcome to Blackjack! Get ready to play against the dealer.")


st.subheader("Game Settings")

# Widget 1: Choose difficulty
difficulty = st.selectbox(
    "Choose your difficulty:",
    ["Easy", "Medium", "Hard"]
)

# Widget 2: Choose starting chips
starting_chips = st.slider(
    "Choose your starting chips:",
    min_value=100,
    max_value=1000,
    value=500,
    step=100
)

# Dynamic output based on user selections
st.subheader("Your Game Setup")

st.write(f"Difficulty selected: {difficulty}")
st.write(f"Starting chips: ${starting_chips}")

if difficulty == "Easy":
    st.success("Easy mode selected! Great for beginners.")
elif difficulty == "Medium":
    st.info("Medium mode selected! Get ready for a challenge.")
else:
    st.warning("Hard mode selected! Good luck!")


import random


st.subheader("Play Blackjack")

# Create a deck of cards
deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4

# Calculate hand total, accounting for Aces
def calculate_total(cards):
    total = sum(cards)
    aces = cards.count(11)

    while total > 21 and aces > 0:
        total -= 10
        aces -= 1

    return total


# Display playing cards with suits

# Display playing cards with suits and colors
def display_cards(cards):
    suits = ["♠", "♥", "♦", "♣"]
    card_html = []

    for i, card in enumerate(cards):
        suit = suits[i % 4]
        value = "A" if card == 11 else str(card)
        color = "#d62828" if suit in ["♥", "♦"] else "#111111"

        card_html.append(
            f'<div style="background:white; color:{color}; '
            f'border:2px solid #ddd; border-radius:12px; '
            f'width:85px; height:125px; padding:10px; '
            f'text-align:center; box-sizing:border-box;">'
            f'<div style="font-size:20px; font-weight:bold;">'
            f'{value} {suit}</div>'
            f'<div style="font-size:42px; margin-top:10px;">'
            f'{suit}</div></div>'
        )

    html = (
        '<div style="display:flex; gap:12px; flex-wrap:wrap;">'
        + "".join(card_html)
        + "</div>"
    )

    st.markdown(html, unsafe_allow_html=True)


# Display the dealer's hidden card
def display_hidden_card():
    st.markdown(
        '<div style="background:#173b75; color:white; '
        'border:3px solid #ffffff; border-radius:12px; '
        'width:85px; height:125px; padding:10px; '
        'display:flex; align-items:center; justify-content:center; '
        'box-sizing:border-box; font-size:38px;">'
        '♠'
        '</div>',
        unsafe_allow_html=True
    )


# Initialize game state
if "player_cards" not in st.session_state:
    st.session_state.player_cards = []

if "dealer_cards" not in st.session_state:
    st.session_state.dealer_cards = []

if "game_over" not in st.session_state:
    st.session_state.game_over = True

if "result" not in st.session_state:
    st.session_state.result = ""

# Deal a new game
if st.button("Deal Cards"):
    cards = random.sample(deck, 4)
    st.session_state.player_cards = cards[:2]
    st.session_state.dealer_cards = cards[2:]
    st.session_state.game_over = False
    st.session_state.result = ""

    if calculate_total(st.session_state.player_cards) == 21:
        st.session_state.game_over = True
        st.session_state.result = "Blackjack! You win!"

# Display current game
if st.session_state.player_cards:
    st.markdown("### Your Hand")
    display_cards(st.session_state.player_cards)
    st.write(
        "Your total:",
        calculate_total(st.session_state.player_cards)
    )

    if not st.session_state.game_over:
        
        st.markdown("### Dealer's Hand")

        dealer_col1, dealer_col2 = st.columns([1, 5])

        with dealer_col1:
            display_cards([st.session_state.dealer_cards[0]])

        with dealer_col2:
            display_hidden_card()


        col1, col2 = st.columns(2)

        with col1:
            if st.button("Hit"):
                st.session_state.player_cards.append(
                    random.choice(deck)
                )

                if calculate_total(st.session_state.player_cards) > 21:
                    st.session_state.game_over = True
                    st.session_state.result = "Bust! Dealer wins."

                st.rerun()

        with col2:
            if st.button("Stand"):
                while calculate_total(
                    st.session_state.dealer_cards
                ) < 17:
                    st.session_state.dealer_cards.append(
                        random.choice(deck)
                    )

                player_total = calculate_total(
                    st.session_state.player_cards
                )
                dealer_total = calculate_total(
                    st.session_state.dealer_cards
                )

                if dealer_total > 21:
                    result = "Dealer busts! You win!"
                elif player_total > dealer_total:
                    result = "You win!"
                elif player_total < dealer_total:
                    result = "Dealer wins!"
                else:
                    result = "It's a tie!"

                st.session_state.result = result
                st.session_state.game_over = True
                st.rerun()

    if st.session_state.game_over:
        
        st.markdown("### Dealer's Hand")
        display_cards(st.session_state.dealer_cards)

        st.write(
            "Dealer's total:",
            calculate_total(st.session_state.dealer_cards)
        )
        st.info(st.session_state.result)
