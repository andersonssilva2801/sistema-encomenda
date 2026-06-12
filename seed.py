"""
Script de Carga Inicial (Seed)

Cria o banco de dados e insere os dados iniciais:
- 1 usuário administrador padrão (admin / admin123)
- Marketplaces de exemplo
- Transportadoras de exemplo
- Funcionários de exemplo

Uso:
    python seed.py
"""

import os
import sys

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.extensions import db
from app.models.usuario import Usuario
from app.models.marketplace import Marketplace
from app.models.transportadora import Transportadora
from app.models.funcionario import Funcionario


def seed_database():
    """Executa a carga inicial do banco de dados."""

    app = create_app()

    with app.app_context():
        # Cria todas as tabelas
        db.create_all()
        print('✅ Tabelas criadas com sucesso!')

        # =============================================
        # USUÁRIO ADMINISTRADOR
        # =============================================
        admin_existente = Usuario.query.filter_by(login='admin').first()
        if not admin_existente:
            admin = Usuario(
                nome='Administrador',
                login='admin',
                perfil='administrador',
                ativo=True
            )
            admin.set_senha('admin123')
            db.session.add(admin)
            print('✅ Usuário administrador criado (login: admin / senha: admin123)')
        else:
            print('ℹ️  Usuário administrador já existe, pulando...')

        # =============================================
        # MARKETPLACES DE EXEMPLO
        # =============================================
        marketplaces_exemplo = [
            {'nome': 'Mercado Livre', 'nome_conta': 'ML Oficial'},
            {'nome': 'Amazon', 'nome_conta': 'Amazon BR'},
            {'nome': 'Shopee', 'nome_conta': 'Shopee Store'},
            {'nome': 'Magazine Luiza', 'nome_conta': 'Magalu'},
        ]

        for mp_data in marketplaces_exemplo:
            existente = Marketplace.query.filter_by(nome=mp_data['nome']).first()
            if not existente:
                mp = Marketplace(**mp_data)
                db.session.add(mp)
                print(f'✅ Marketplace criado: {mp_data["nome"]}')
            else:
                print(f'ℹ️  Marketplace já existe: {mp_data["nome"]}')

        # =============================================
        # TRANSPORTADORAS DE EXEMPLO
        # =============================================
        transportadoras_exemplo = [
            {'nome': 'Correios', 'valor_padrao': 18.50},
            {'nome': 'Jadlog', 'valor_padrao': 25.90},
            {'nome': 'Loggi', 'valor_padrao': 22.00},
            {'nome': 'Total Express', 'valor_padrao': 19.75},
        ]

        for tr_data in transportadoras_exemplo:
            existente = Transportadora.query.filter_by(nome=tr_data['nome']).first()
            if not existente:
                tr = Transportadora(**tr_data)
                db.session.add(tr)
                print(f'✅ Transportadora criada: {tr_data["nome"]}')
            else:
                print(f'ℹ️  Transportadora já existe: {tr_data["nome"]}')

        # =============================================
        # FUNCIONÁRIOS DE EXEMPLO
        # =============================================
        funcionarios_exemplo = [
            {'nome': 'João da Silva'},
            {'nome': 'Maria Santos'},
            {'nome': 'Pedro Lima'},
        ]

        for func_data in funcionarios_exemplo:
            existente = Funcionario.query.filter_by(nome=func_data['nome']).first()
            if not existente:
                func = Funcionario(**func_data)
                db.session.add(func)
                print(f'✅ Funcionário criado: {func_data["nome"]}')
            else:
                print(f'ℹ️  Funcionário já existe: {func_data["nome"]}')

        # =============================================
        # COMMIT FINAL
        # =============================================
        try:
            db.session.commit()
            print('\n🎉 Carga inicial concluída com sucesso!')
            print('=' * 50)
            print('📋 Resumo:')
            print(f'   Usuários:        {Usuario.query.count()}')
            print(f'   Marketplaces:    {Marketplace.query.count()}')
            print(f'   Transportadoras: {Transportadora.query.count()}')
            print(f'   Funcionários:    {Funcionario.query.count()}')
            print('=' * 50)
            print('\n🔑 Acesso padrão:')
            print('   Login: admin')
            print('   Senha: admin123')
            print('\n⚠️  IMPORTANTE: Altere a senha do administrador após o primeiro acesso!')
        except Exception as e:
            db.session.rollback()
            print(f'\n❌ Erro ao executar carga inicial: {e}')
            sys.exit(1)


if __name__ == '__main__':
    seed_database()
