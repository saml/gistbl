local sundown = require('sundown')
print(sundown.markdown([[
# hello world

this is a test markdown entry.

    some code is here
    a = b + 1
    <script>alert(1)</script>

1. some list here
1. 유니코드
    * bleh another
    * yup
1. hello world

`
trying github flavored
not sure if it'll work
`

bye.

$$ a \in b $$

<script>alert(2)</script>]]))
