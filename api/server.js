const express=require("express");
const cors=require("cors");
const fs=require("fs");
const path=require("path");

const app=express();
app.use(cors());

//lê o json gerado pelo script python
const caminho=path.join(__dirname,"..","coleta-python","populacao_estados.json");
const estados=JSON.parse(fs.readFileSync(caminho,"utf-8"));

//GET/estados ou /estados?regiao=Nordeste
app.get("/estados",(req,res)=>{
    const {regiao}=req.query;
    const resultado=regiao
        ? estados.filter((e)=> e.regiao.toLowerCase()===regiao.toLowerCase())
        : estados;
    res.json(resultado);
    
});
//GET/resumo -> população total por região
app.get("/resumo",(req,res)=>{
    const porRegiao={};
    for(const e of estados){
        porRegiao[e.regiao]=(porRegiao[e.regiao]||0)+e.populacao;
    }
    res.json(porRegiao)
});

const PORTA=3000;
app.listen(PORTA,()=>{
    console.log(`API rodando em http://localhost:${PORTA}`);
});
