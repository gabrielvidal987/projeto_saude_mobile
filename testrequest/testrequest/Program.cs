using System;
using System.Net.Http;
using System.Security.Cryptography.X509Certificates;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;
class Program
{
    static async Task Delete_method(string[] args)
    {
        using (HttpClient client = new HttpClient())
        {
            try
            {
                HttpResponseMessage response = await client.DeleteAsync("https://api.exemplo.com/usuarios/123");

                if (response.IsSuccessStatusCode)
                {
                    Console.WriteLine("Usuário excluído com sucesso");
                }
                else
                {
                    Console.WriteLine("Falha ao excluir usuário");
                }
            }
            catch (HttpRequestException e)
            {
                Console.WriteLine($"Erro: {e.Message}");
            }
        }
    }
    static async Task Put_method(string[] args)
    {
        using (HttpClient client = new HttpClient())
        {
            try
            {
                // Dados para atualização
                var updatedUser = new { nome = "João Silva Atualizado", email = "joao.novoemail@exemplo.com" };
                string json = Newtonsoft.Json.JsonConvert.SerializeObject(updatedUser);  // Serializa para JSON

                StringContent content = new StringContent(json, Encoding.UTF8, "application/json");

                HttpResponseMessage response = await client.PutAsync("https://api.exemplo.com/usuarios/123", content);
                response.EnsureSuccessStatusCode();  // Lança exceção em caso de falha

                string responseBody = await response.Content.ReadAsStringAsync();
                Console.WriteLine("Usuário atualizado: " + responseBody);
            }
            catch (HttpRequestException e)
            {
                Console.WriteLine($"Erro: {e.Message}");
            }
        }
    }
    static async Task Post_method(string[] args)
    {
        using (HttpClient client = new HttpClient())
        {
            try
            {
                // Dados que queremos enviar
                var newUser = new { nome = "João Silva", email = "joao@exemplo.com" };
                string json = Newtonsoft.Json.JsonConvert.SerializeObject(newUser);  // Serializa o objeto para JSON

                StringContent content = new StringContent(json, Encoding.UTF8, "application/json");

                HttpResponseMessage response = await client.PostAsync("https://api.exemplo.com/usuarios", content);
                response.EnsureSuccessStatusCode();  // Lança exceção em caso de falha

                string responseBody = await response.Content.ReadAsStringAsync();
                Console.WriteLine("Novo usuário criado: " + responseBody);
            }
            catch (HttpRequestException e)
            {
                Console.WriteLine($"Erro: {e.Message}");
            }
        }
    }
    static async Task<string> Get_method(string[] args)
    {
        using (HttpClient client = new HttpClient())
        {
            try
            {
                HttpResponseMessage response = await client.GetAsync("http://217.77.9.21:3000/api/unidades");
                response.EnsureSuccessStatusCode();  // Lança uma exceção se a resposta for um erro (não 2xx)

                string responseBody = await response.Content.ReadAsStringAsync();
                return responseBody;
            }
            catch (HttpRequestException e)
            {
                Console.WriteLine($"Erro: {e.Message}");
                return e.Message;
            }
        }
    }
    static async Task Main(string[] args)
    {
        /* o bd_select retornado é um json contendo uma lista de dicionarios. cada dicionario será uma linha 
         do bd. a lista será a pesquisa completa do bd. então cada item da lista é um dicionario. 
         cada dicionario sendo uma linha do retorno do bd */
        string bd_select = await Get_method(args);
        List<Dictionary<string, object>> listaDeDicionarios = JsonConvert.DeserializeObject<List<Dictionary<string, object>>>(bd_select);
        foreach (var dict in listaDeDicionarios)
        {
            Console.WriteLine(dict["id_sys"]);
            Console.WriteLine(dict["nome_atividade"]);
            Console.WriteLine(dict["caminho_foto_atividade"]);
        }
    }
}
