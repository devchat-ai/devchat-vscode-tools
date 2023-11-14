import os
import sys
from chat.ask_codebase.chains.smart_qa import SmartQA


def query(question, lsp_brige_port):
    root_path = os.getcwd()
    
    # Create an instance of SmartQA
    smart_qa = SmartQA(root_path)

    # Use SmartQA to get the answer
    answer = smart_qa.run(question=question, verbose=False, dfs_depth=3, dfs_max_visit=10, bridge_url=f'http://localhost:{lsp_brige_port}' )

    # Print the answer
    print(answer[0])
    print(f"\n\n/***ask-code has costed approximately ${int(float(answer[2]['token_usage']['total_cost'])/0.7*10000)/10000} USD for this question.***")


def main():
    try:
        if len(sys.argv) < 4:
            print("Usage: python index_and_query.py query [question] [port]")
            sys.exit(1)
        
        question = sys.argv[2]
        port = sys.argv[3]
        query(question, port)
        sys.exit(0)
    except Exception as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()