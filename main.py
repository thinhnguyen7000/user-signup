
#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re


# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>SignUp</title>
    <style type="text/css">
        .label {text-align: right}
        .error {color: red;}
    </style>
</head>
<body>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""
def valid_username(self, username):
    user_re = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return username and user_re.match(username)


def valid_password(self, password):
    pass_re = re.compile(r"^.{3,20}$")
    return password and pass_re.match(password)


def valid_email(self, email):
    email_re = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
    return not email or email_re.match(email)

form= """

<!DOCTYPE html>
<html>
<head>
    <title>SignUp</title>
    <style type="text/css">
        .label {text-align: left}
        .error {color: red;}
    </style>
</head>
<body>
    <h2>SignUp</h2>
    <form method= "post">
    <table>
        <tr>
            <td class= "label">
                Username
            </td>
            <td> <input type="text" name="username" value="%(username)s">
            </td>
            <td class="error">
                %(username_error)s
            </td>
        </tr>

        <tr>
            <td class= "label">
                Password
            </td>
            <td> <input type="password" name="password" value="">
            </td>
            <td class="error">
                %(password_error)s
            </td>
        </tr>

        <tr>
            <td class= "label">
                Verify Password
            </td>
            <td> <input type="password" name="verify" value="">
            </td>
            <td class="error">
                %(verify_error)s
            </td>
        </tr>

        <tr>
            <td class= "label">
                Email (optional)
            </td>
            <td> <input type="text" name="email" value="%(email)s">
            </td>
            <td class="error">
                %(email_error)s
            </td>
        </tr>
    </table>

    <input type="submit">
</form>

</body>
</html>
"""




class MainHandler(webapp2.RequestHandler):
    def write_form(self, username="", username_error="", password_error="",email="",verify_error="", email_error=""):
        self.response.out.write(form % { "username": username,
                                        "email": email,
                                        "username_error": username_error,
                                        "password_error": password_error,
                                        "verify_error": verify_error,
                                        "email_error": email_error
                                        })



    def valid_username(self, username):
        user_re = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        return username and user_re.match(username)


    def valid_password(self, password):
        pass_re = re.compile(r"^.{3,20}$")
        return password and pass_re.match(password)


    def valid_email(self, email):
        email_re = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
        return email_re.match(email)


    def get(self):

        self.write_form()


    def post(self):

        username = self.request.get("username")
        username_is_valid = self.valid_username(username)

        password = self.request.get("password")
        password_is_valid = self.valid_password(password)
        password_error = ""

        verify = self.request.get("verify")
        verify_error = ""

        email = self.request.get("email")
        email_is_valid = self.valid_email(email)
        email_error = ""

        username_error =""
        have_error = False

        if not username_is_valid: #and valid_password(self, password) and password != verify and valid_email(self, email)):
            username_error ="That's not a valid username."
            have_error = True

        if not password_is_valid:
            password_error = "That wasn't a valid password."
            have_error = True

        if password != verify:
            verify_error = "Your passwords didn't match."
            have_error = True

        if email and email_is_valid:
            email_error = "That's not a valid email."
            have_error = True

        if have_error:
            self.write_form(username = username, email = email, username_error = username_error,
                            password_error = password_error,verify_error = verify_error,
                            email_error = email_error)
        else:
            self.redirect('/welcome?username=%s' % username)
            return


class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        self.response.out.write('<h1> Welcome, %s</h1>' % username)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', Welcome)
], debug=True)
