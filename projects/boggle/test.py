from unittest import TestCase
from app import app
from flask import session, jsonify
from boggle import Boggle
import json


app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class FlaskTests(TestCase):

    def setUp(self):
       self.client = app.test_client()
    
    def test_home(self):
        resp = self.client.get("/")
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn("Enjoy!", html)

    def test_start_game(self):
        with self.client:
            resp = self.client.get("/play")
            html = resp.get_data(as_text=True)
            

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Enter a word!", html)
            self.assertIn("Submit", html)
            self.assertIn("<td>", html)
            self.assertIn('board', session)
    
    def test_real_word(self):
            with self.client:
                with  self.client.session_transaction() as sess:
            
                    sess['board'] = [["C", "A", "T", "T", "T"], 
                                    ["C", "A", "T", "T", "T"], 
                                    ["C", "A", "T", "T", "T"], 
                                    ["C", "A", "T", "T", "T"], 
                                    ["C", "A", "T", "T", "T"]]
                resp = self.client.get("/real_word", query_string={"word": "snake"})
                good_resp = self.client.get("/real_word", query_string={"word": "cat"})
                bad_resp = self.client.get("/real_word", query_string={'word':'iufahlwghqriphgqiupgqwip'})
                html = bad_resp.get_data(as_text=True)

                
                
                self.assertIn("not", html)
                self.assertEqual(resp.json['result'], "not-on-board")
                self.assertEqual(good_resp.json['result'], "ok")
                self.assertIn('board', session)
                self.assertEqual(resp.status_code, 200)
                self.assertIn("result", html)

    
    def test_end_game(self):
        with self.client:
            with  self.client.session_transaction() as sess:
                sess['highest_score'] = 98
                sess['times_played'] = 0
            resp = self.client.post("/end_game",  json=({"score": 99}))
            
            
            self.assertIn('highest_score', session)
            self.assertIn('times_played', session)
            
            self.assertEqual(session['highest_score'], 99)
            self.assertEqual(session['times_played'], 1)
            




if __name__ == '__main__':
    unittest.main()