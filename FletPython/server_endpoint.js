const express = require('express');
const mysql = require('mysql2');
const cors = require('cors');
const app = express();
const PORT = 3000;

// Configuração da conexão com o banco de dados
const db = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: 'Vid@l9871',
    database: 'projeto_saude'
});

// Conectar ao banco de dados
db.connect(err => {
    if (err) throw err;
    console.log('             Conectado ao banco de dados!');
});

// Habilitar CORS
app.use(cors());

// Habilitar o middleware para parsing do corpo das requisições
app.use(express.json()); // Mover essa linha para cima

// Endpoint para receber os nomes das atividades
app.get('/api/usuarios', (req, res) => {
    // Extrai o nome da atividade da URL
    console.log(`\n\nRequisição para pegar os dados de todos os usuários`)
    const sql = `SELECT * FROM usuarios;;`
    console.log(`comando sql -> ${sql}`)
    db.query(sql, (err, results) => {
        if (err) {
            console.error('Erro ao consultar o banco de dados:', err);
            return res.status(500).json({ erro: 'Erro no servidor' });
        }
        res.json(results);
    });
});

// Endpoint para inserir um novo usuário
app.post('/api/novousuario', (req, res) => {
    // Pega os dados do novo usuário que vieram na requisição
    const { nome, senha, nivel_acesso } = req.body;
    console.log(`\n\nRequisição para criar um novo usuário: ${nome}`);
    // Verifica se todos os dados necessários foram fornecidos
    if (!nome || !senha || !nivel_acesso) {
        return res.status(400).json({ error: 'Todos os campos são necessários (nome, senha, nivel_acesso)' });
    }
    // Cria o comando SQL para inserir o novo usuário
    const sql = `INSERT INTO usuarios (nome, senha, nivel_acesso) VALUES ('${nome}', '${senha}', '${nivel_acesso}');`;
    console.log(`Comando SQL: ${sql}`);
    // Executa o comando SQL
    db.query(sql, (err, result) => {
        // Caso dê erro, retorna o erro
        if (err) {
            console.error('Erro ao inserir novo usuário:', err);
            return res.status(500).json({ error: 'Erro no servidor' });
        }
        // Retorna a resposta de sucesso com a mensagem
        return res.json({
            mensagem: 'Usuário criado com sucesso!',
            userId: result.insertId,  // Retorna o ID do novo usuário inserido (caso o banco tenha um auto incremento)
        });
    });
});

// Endpoint para alterar a senha do usuário
app.put('/api/alterarsenha', (req, res) => {
    // Pega o nome, id_sys e nova_senha que vieram na requisição
    const { id_sys, nome, nova_senha } = req.body;
    console.log(`\n\nRequisição para alterar a senha do usuário ${nome} ID: ${id_sys}`);
    // Cria o comando SQL para atualizar a senha
    const sql = `UPDATE usuarios SET senha = '${nova_senha}' WHERE nome = '${nome}' and id_sys = ${id_sys};`;
    console.log(`Comando SQL: ${sql}`);
    // Executa a query no banco de dados
    db.query(sql, (err, result) => {
        // Caso dê erro, retorna o erro
        if (err) {
            console.error('Erro ao alterar senha de usuário:', err);
            return res.status(500).json({ error: 'Erro no servidor' });
        }
        // Caso não encontre o usuário para atualizar
        if (result.affectedRows === 0) {
            return res.status(404).json({ error: 'Usuário não encontrado' });
        }
        // Retorna sucesso se a senha for alterada com sucesso
        return res.json({
            mensagem: 'Senha alterada com sucesso!',
        });
    });
});

// Endpoint para deletar um usuário
app.delete('/api/deletarusuario', (req, res) => {
    // Pega o id_sys e nome que vieram na requisição
    const id_sys = req.body.id_sys;
    const nome = req.body.nome;
    console.log(`\n\nRequisição para deletar o usuário ${nome} ID: ${id_sys}`);
    // Cria o comando SQL para deletar o usuário especificado
    const sql = `DELETE FROM usuarios WHERE nome = '${nome}' and id_sys = ${id_sys};`;
    console.log(`Comando SQL: ${sql}`);
    db.query(sql, (err, result) => {
        // Caso dê erro, irá informar o erro
        if (err) {
            console.error('Erro ao deletar usuário:', err);
            return res.status(500).json({ error: 'Erro no servidor' });
        }
        // Caso o usuário não exista, será retornado um erro de "Usuário não encontrado"
        if (result.affectedRows === 0) {
            return res.status(404).json({ error: 'Usuário não encontrado' });
        }
        // Deletado com sucesso, retorna uma mensagem de sucesso
        return res.json({
            mensagem: 'Usuário deletado com sucesso!',
        });
    });
});

// Iniciar o servidor
app.listen(PORT, () => {
    console.log(`------------Servidor rodando na porta ${PORT}------------`);
});