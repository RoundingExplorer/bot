@client.event
async def on_message(message):
   global Hangman, guessed, tries, guessed_letters, channel, word, word_completion, guessed_words

   if message.content.startswith('.hm'):
       Hangman = True
       print("hangman started")
       channel = message.channel
       word = get_word()
       word_completion = "_" * len(word)
       guessed = False
       guessed_letters = []
       guessed_words = []
       tries = 6

       await channel.send("Let's play hangman")
       await channel.send(display_hangman(tries))
       await channel.send(word_completion)

   elif message.content.startswith('.hm quit'):
       Hangman = False

   if Hangman:
       print(str(guessed) + str(tries))
       if not guessed and tries > 0:

           def check(m):
               if any(c.isalpha() for c in m.content) and len(str(m)) == 1:
                   return m.content == message

           print('Running')
           guess = await client.wait_for('message', check=check)
           print(str(guess))

           if len(str(guess)) == 1:
               if guess in guessed_letters:
                   await channel.send("You already guessed the letter", guess)
               elif guess not in word:
                   await channel.send(guess, "is not in the word.")
                   tries -= 1
                   guessed_letters.append(guess)
               else:
                   await channel.send("Good job,", guess, "is in the word!")
                   guessed_letters.append(guess)
                   word_as_list = list(word_completion)
                   indices = [i for i, letter in enumerate(word) if letter == guess]
                   for index in indices:
                       word_as_list[index] = guess
                   word_completion = "".join(word_as_list)
                   if "_" not in word_completion:
                    guessed = True
           elif len(guess) == len(word) and guess.isalpha():
               if guess in guessed_words:
                   await channel.send("You already guessed the word", guess)
               elif guess != word:
                   await channel.send(guess, "is not the word.")
                   tries -= 1
                   guessed_words.append(guess)
               else:
                   guessed = True
                   word_completion = word
           else:
               await channel.send("Not a valid guess.")
           await channel.send(display_hangman(tries))
           await channel.send(word_completion)

       if guessed:
           await channel.send("Congrats, you guessed the word! You win!")
       else:
           await channel.send("Sorry, you ran out of tries. The word was " + word + ". Maybe next time!")
